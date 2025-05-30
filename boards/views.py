from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView, FormView
from django.urls import reverse, reverse_lazy
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.utils.text import slugify
from django.utils import timezone
from django.views import View
from datetime import timedelta
import json

from . import models
from .forms import BoardMemberForm, BoardForm, BoardInviteForm


class BoardListView(LoginRequiredMixin, ListView):
    """
    Exibe detalhes do board, incluindo colunas e tarefas associadas.
    Acesso restrito a membros com permissão mínima de visualização.
    """

    model = models.Board
    template_name = 'boards/dashboard.html'
    context_object_name = 'boards'

    def get_queryset(self):
        """
        Retorna queryset com boards do usuário logado.
        """
        return models.Board.objects.filter(memberships__member=self.request.user).distinct()



class BoardDetailView(LoginRequiredMixin, DetailView):
    """
    Exibe detalhes do board, incluindo colunas e tarefas associadas.
    Acesso restrito a membros com permissão mínima de visualização.
    """

    model = models.Board
    template_name = 'boards/board_details.html'
    context_object_name = 'board'

    def get_queryset(self):
        """
        Retorna o board filtrado pelo slug e username, garantindo que o usuário seja membro.
        """
        return models.Board.objects.filter(
            memberships__member__username=self.request.user,
            slug=self.kwargs['slug']
        )

    def get_context_data(self, **kwargs):
        """
        Adiciona colunas e tarefas do board no contexto.
        """
        context = super().get_context_data(**kwargs)
        context['columns'] = self.object.column_set.all()
        context['tasks'] = models.Task.objects.filter(column__board=self.object)
        return context
    
    def dispatch(self, request, *args, **kwargs):
        """
        Garante que o usuário tenha permissão de acesso ao board.
        Permissões válidas: owner, moderator, editor, viewer.
        Caso contrário, retorna 403 (proibido).
        """

        board = get_object_or_404(
            models.Board,
            slug=kwargs['slug'],
            memberships__member=request.user
        )

        member = models.BoardMember.objects.filter(
            board=board,
            member=request.user,
            permission__in=['owner', 'moderator', 'editor', 'viewer']
        ).first()

        if not member:
            return HttpResponseForbidden("Você não tem acesso a esse board.")
        
        return super().dispatch(request, *args, **kwargs)



class BoardCreateView(LoginRequiredMixin, View):
    """
    Cria novo board. Apenas GET e POST para formulário.
    Após salvar, adiciona o criador como membro com permissão 'owner'.
    Também cria uma coluna padrão ao criar o board.
    """

    def get(self, request):
        form = BoardForm()
        return render(request, 'boards/new_board.html', {'form': form})

    def post(self, request):
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.created_by = request.user
            board.save()

            # Adiciona criador como membro 'owner'
            models.BoardMember.objects.create(
                board=board,
                member=request.user,
                permission='owner'
            )

            # Cria coluna padrão
            models.Column.objects.create(
                board=board,
                name='Nova Coluna',
                order=1
            )

            messages.success(request, 'Board criado com sucesso.')
            return redirect('dashboard')
        return render(request, 'boards/new_board.html', {'form': form})


class BoardEditView(LoginRequiredMixin, View):
    """
    Edita board, gerencia membros e gera convite.
    Restrições de permissão aplicadas conforme solicitado.
    """

    @staticmethod
    def user_can_edit_board(user, board):
        try:
            membership = models.BoardMember.objects.get(member=user, board=board)
            return membership.permission in ['owner', 'moderator']
        except models.BoardMember.DoesNotExist:
            return False

    @staticmethod
    def user_can_invite(user, board):
        try:
            membership = models.BoardMember.objects.get(member=user, board=board)
            return membership.permission in ['owner', 'moderator']
        except models.BoardMember.DoesNotExist:
            return False

    def get(self, request, username, slug):
        board = get_object_or_404(models.Board, slug=slug, created_by__username=username)
        if not self.user_can_edit_board(request.user, board):
            return redirect('dashboard')

        board_form = BoardForm(instance=board)
        members = models.BoardMember.objects.filter(board=board)
        invite_form = BoardInviteForm()

        context = {
            'board': board,
            'board_form': board_form,
            'members': members,
            'invite_form': invite_form,
        }
        return render(request, 'boards/board_edit.html', context)

    def post(self, request, username, slug):
        board = get_object_or_404(models.Board, slug=slug, created_by__username=username)
        if not self.user_can_edit_board(request.user, board):
            return redirect('dashboard')

        if 'save_board' in request.POST:
            board_form = BoardForm(request.POST, instance=board)
            members = models.BoardMember.objects.filter(board=board)
            invite_form = BoardInviteForm()
            if board_form.is_valid():
                board_form.save()
                messages.success(request, 'Board atualizado.')
                return redirect(reverse('board_edit', args=[username, slug]))

            context = {
                'board': board,
                'board_form': board_form,
                'members': members,
                'invite_form': invite_form,
            }
            return render(request, 'boards/board_edit.html', context)

        elif 'create_invite' in request.POST:
            if not self.user_can_invite(request.user, board):
                messages.error(request, 'Sem permissão para gerar convites.')
                return redirect(reverse('board_edit', args=[username, slug]))

            invite_form = BoardInviteForm(request.POST)
            members = models.BoardMember.objects.filter(board=board)
            board_form = BoardForm(instance=board)
            if invite_form.is_valid():
                permission = invite_form.cleaned_data['permission']
                if permission == 'owner':
                    messages.error(request, 'Permissão owner não permitida para convites.')
                    return redirect(reverse('board_edit', args=[username, slug]))

                invite = models.BoardInvite.objects.create(
                    board=board,
                    invited_by=request.user,
                    expires_at=timezone.now() + timedelta(days=7),
                    permission=permission
                )
                invite_link = request.build_absolute_uri(
                    reverse('board_invite_accept', args=[str(invite.token)])
                )
                messages.success(request, f'Link de convite gerado: {invite_link}')
                return redirect(reverse('board_edit', args=[username, slug]))
            else:
                context = {
                    'board': board,
                    'board_form': board_form,
                    'members': members,
                    'invite_form': invite_form,
                }
                return render(request, 'boards/board_edit.html', context)

        elif 'remove_member' in request.POST:
            member_id = request.POST.get('remove_member')
            try:
                member = models.BoardMember.objects.get(id=member_id, board=board)

                if member.permission == 'owner':
                    messages.error(request, 'Não é permitido remover o proprietário (owner).')

                elif member.member == request.user:
                    if 'confirm_leave' not in request.POST:
                        messages.error(request, 'Confirme que deseja sair do board.')
                    else:
                        member.delete()
                        messages.success(request, 'Você saiu do board.')
                        return redirect('dashboard')

                else:
                    member.delete()
                    messages.success(request, 'Membro removido.')

            except models.BoardMember.DoesNotExist:
                messages.error(request, 'Membro não encontrado.')

            return redirect(reverse('board_edit', args=[username, slug]))

        else:
            return redirect(reverse('board_edit', args=[username, slug]))



class UpdateBoardView(LoginRequiredMixin, UpdateView):
    """
    Atualiza o título e descrição do board.
    Acesso restrito a membros com permissão de proprietário ou moderador.
    """
    model = models.Board
    fields = ['name', 'description']
    template_name = 'boards/board_update.html'

    def get_object(self, queryset=None):
        queryset = self.model.objects.filter(
            slug=self.kwargs['slug'], 
            memberships__member=self.request.user
        )
        
        board = super().get_object(queryset)
        has_permission = models.BoardMember.objects.filter(
            board=board,
            member=self.request.user,
            permission__in=['owner', 'moderator']
        ).exists()
        if not has_permission:
            raise Http404("Você não tem permissão para editar esse board.")
        return board

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse('board_detail', kwargs={
            'username': self.kwargs['username'],
            'slug': self.kwargs['slug']
        })



class DeleteBoardView(LoginRequiredMixin, DeleteView):
    """
    Remove um board. Acesso restrito ao proprietário e apenas se for membro.
    """
    model = models.Board
    template_name = 'boards/board_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        queryset = self.model.objects.filter(
            slug=self.kwargs['slug'],
            memberships__member=self.request.user
        )
        board = queryset.first()
        if not board:
            raise Http404("Board não encontrado.")

        has_permission = models.BoardMember.objects.filter(
            board=board,
            member=self.request.user,
            permission='owner'
        ).exists()
        if not has_permission:
            raise Http404("Você não tem permissão para excluir esse board.")

        return board

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        board = self.get_object()
        try:
            permission = board.memberships.get(member=self.request.user).permission
        except models.BoardMember.DoesNotExist:
            permission = None
        context['user_permission'] = permission
        context['board'] = board
        return context



class AddBoardMemberView(LoginRequiredMixin, CreateView):
    """
    Adiciona membro a um board.
    Apenas proprietários e moderadores podem adicionar membros.
    """
    model = models.BoardMember
    form_class = BoardMemberForm
    template_name = 'boards/add_members.html'

    def dispatch(self, request, *args, **kwargs):
        self.board = get_object_or_404(
            models.Board,
            slug=self.kwargs['slug'],
            memberships__member=request.user  # Garante que o usuário é membro
        )

        has_permission = models.BoardMember.objects.filter(
            board=self.board,
            member=request.user,
            permission__in=['owner', 'moderator']
        ).exists()

        if not has_permission:
            raise Http404("Você não tem permissão para adicionar membros a esse board.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.board = self.board

        # Só permite permissões que o usuário atual pode conceder
        user_permission = models.BoardMember.objects.get(
            board=self.board,
            member=self.request.user
        ).permission

        allowed_permissions = {
            'owner': ['moderator', 'editor', 'viewer'],
            'moderator': ['editor', 'viewer']
        }

        if form.instance.permission not in allowed_permissions.get(user_permission, []):
            form.instance.permission = 'viewer'  # padrão seguro

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board

        board_member = models.BoardMember.objects.get(
            board=self.board,
            member=self.request.user
        )
        user_permission = board_member.permission
        context['user_permission'] = user_permission

        allowed = {
            'owner': ['moderator', 'editor', 'viewer'],
            'moderator': ['editor', 'viewer']
        }.get(user_permission, [])

        # Filtra as opções do campo diretamente
        form = context['form']
        form.fields['permission'].choices = [
            (value, label)
            for value, label in form.fields['permission'].choices
            if value in allowed
        ]

        context['allowed_permissions'] = allowed
        return context

    def get_success_url(self):
        return reverse('board_detail', kwargs={
            'username': self.board.created_by.username,
            'slug': self.board.slug
        })



class CreateBoardInviteView(LoginRequiredMixin, View):
    """
    Cria convite para usuário entrar no board via token.
    Restrito a proprietários e moderadores.
    """

    def get(self, request, username, slug):
        form = BoardInviteForm()
        return render(request, 'boards/invite_form.html', {'form': form, 'username': username, 'slug': slug})

    def post(self, request, username, slug):
        board = get_object_or_404(
            models.Board,
            slug=slug,
            memberships__member=request.user
        )

        has_permission = models.BoardMember.objects.filter(
            board=board,
            member=request.user,
            permission__in=['owner', 'moderator']
        ).exists()

        if not has_permission:
            messages.error(request, "Sem permissão para convidar membros.")
            return redirect('board_detail', username=username, slug=slug)

        form = BoardInviteForm(request.POST)
        if form.is_valid():
            permission = form.cleaned_data['permission']

            invite = models.BoardInvite.objects.create(
                board=board,
                invited_by=request.user,
                permission=permission,
                expires_at=timezone.now() + timedelta(days=7)
            )

            invite_link = request.build_absolute_uri(
                reverse('board_invite_accept', args=[str(invite.token)])
            )
            messages.success(request, f'Link de convite gerado: {invite_link}')
            return redirect('board_edit', username=username, slug=slug)

        return render(request, 'boards/invite_form.html', {'form': form, 'username': username, 'slug': slug})


class BoardInviteAcceptView(View):
    def get(self, request, token):
        invite = get_object_or_404(models.BoardInvite, token=token)

        if not request.user.is_authenticated:
            login_url = f"{reverse('login')}?next={request.path}"
            return redirect(login_url)

        if invite.is_expired():
            messages.error(request, "Convite expirado.")
            return redirect('dashboard')

        if invite.permission == 'owner':
            messages.error(request, "Permissão 'owner' não permitida via convite.")
            return redirect('dashboard')

        already_member = models.BoardMember.objects.filter(
            board=invite.board,
            member=request.user
        ).exists()

        if not already_member:
            models.BoardMember.objects.create(
                board=invite.board,
                member=request.user,
                permission=invite.permission
            )
            invite.accepted = True
            invite.save()
            messages.success(request, f"Você entrou no board como '{invite.permission}'.")
        else:
            messages.info(request, "Você já faz parte deste board.")

        return redirect(reverse('board_detail', args=[invite.board.created_by.username, invite.board.slug]))


class AddColumnView(LoginRequiredMixin, CreateView):
    """
    Adiciona coluna a um board.
    Apenas proprietários, moderadores e editores podem adicionar.
    Levanta HttpResponseForbidden se sem permissão.
    """
    model = models.Column
    fields = ['name']
    template_name = 'boards/add_column.html'

    def dispatch(self, request, *args, **kwargs):
        self.board = get_object_or_404(
            models.Board,
            created_by__username=self.kwargs['username'],
            slug=self.kwargs['slug']
        )
        has_permission = models.BoardMember.objects.filter(
            board=self.board,
            member=request.user,
            permission__in=['owner', 'moderator', 'editor']
        ).exists()
        if not has_permission:
            return HttpResponseForbidden("Você não tem permissão para editar colunas nesse board.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.board = self.board
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context

    def get_success_url(self):
        return reverse('board_detail', kwargs={
            'username': self.kwargs['username'],
            'slug': self.kwargs['slug']
        })



class EditColumnAjaxView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() != 'post':
            return JsonResponse({'error': 'Método não permitido'}, status=405)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, username, slug, pk):
        try:
            column = models.Column.objects.get(pk=pk, board__slug=slug, board__created_by__username=username)
        except models.Column.DoesNotExist:
            return JsonResponse({'error': 'Coluna não encontrada'}, status=404)

        board = column.board
        try:
            membership = models.BoardMember.objects.get(board=board, member=request.user)
        except models.BoardMember.DoesNotExist:
            return JsonResponse({'error': 'Sem permissão'}, status=403)

        if membership.permission not in ['owner', 'moderator']:
            return JsonResponse({'error': 'Sem permissão'}, status=403)

        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        new_name = data.get('name', '').strip()
        if not new_name:
            return JsonResponse({'error': 'Nome inválido'}, status=400)

        column.name = new_name
        column.save()

        return JsonResponse({'success': True, 'name': column.name})



class DeleteColumnAjaxView(LoginRequiredMixin, View):
    def post(self, request, username, slug, pk):
        try:
            column = models.Column.objects.get(pk=pk, board__slug=slug, board__created_by__username=username)
        except models.Column.DoesNotExist:
            return JsonResponse({'error': 'Coluna não encontrada'}, status=404)

        board = column.board
        
        has_permission = models.BoardMember.objects.filter(
            board=board,
            member=request.user,
            permission__in=['owner', 'moderator']
    ).exists()

        if not has_permission:
            return JsonResponse({'error': 'Sem permissão'}, status=403)

        
        def dispatch(self, request, *args, **kwargs):
            if request.method.lower() != 'post':
                return JsonResponse({'error': 'Método não permitido'}, status=405)
            return super().dispatch(request, *args, **kwargs)

        column.delete()
        return JsonResponse({'success': True})
