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

class BoardPermissionRequiredMixin:
    required_permission = None
    use_membership_filter = True

    def dispatch(self, request, *args, **kwargs):
        board_filter = {'slug': kwargs['slug']}

        if self.use_membership_filter:
            board_filter['memberships__member'] = request.user
        else:
            board_filter['created_by__username'] = kwargs['username']

        board = get_object_or_404(models.Board, **board_filter)

        if not models.BoardMember.user_has_access(board, request.user, self.required_permission):
            return HttpResponseForbidden("Você não tem permissão suficiente para executar essa ação neste board.")

        self.board = board
        return super().dispatch(request, *args, **kwargs)

class AjaxBoardPermissionMixin(BoardPermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() != 'post':
            return JsonResponse({'error': 'Método não permitido'}, status=405)
        
        # Tenta rodar o dispatch da BoardPermissionMixin, que pode retornar HttpResponseForbidden
        response = super().dispatch(request, *args, **kwargs)

        # Se o super().dispatch retornar HttpResponseForbidden, converte em JsonResponse
        if isinstance(response, HttpResponseForbidden):
            return JsonResponse({'error': 'Sem permissão'}, status=403)

        return response

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models

class BoardListView(LoginRequiredMixin, TemplateView):
    template_name = 'boards/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['boards_own'] = models.Board.objects.filter(created_by=user)
        context['boards_joined'] = models.Board.objects.filter(
            memberships__member=user
        ).exclude(created_by=user)

        return context




class BoardDetailView(LoginRequiredMixin, DetailView, BoardPermissionRequiredMixin):
    """
    Exibe detalhes do board, incluindo colunas e tarefas associadas.
    Acesso restrito a membros com permissão mínima de visualização.
    """

    model = models.Board
    template_name = 'boards/board_details.html'
    context_object_name = 'board'

    required_permission = 'viewer'
    use_membership_filter = True

    def get_queryset(self):
        """
        Retorna o board filtrado pelo slug e username, garantindo que o usuário seja membro.
        """
        return models.Board.objects.filter(
            memberships__member=self.request.user,
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
    

class BoardCreateView(LoginRequiredMixin, View):

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

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'id': board.id,
                    'name': board.name,
                    'url': reverse('board_detail', kwargs={
                        'username': board.created_by.username,
                        'slug': board.slug
                    }),
                    'color_theme': board.color_theme,
                    'image_theme': board.background_image  # corrigido
                })

            messages.success(request, 'Board criado com sucesso.')
            return redirect('dashboard')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Nome inválido ou outro erro'}, status=400)

        return render(request, 'boards/new_board.html', {'form': form})


class BoardEditView(LoginRequiredMixin, View, BoardPermissionRequiredMixin):
    """
    Edita board, gerencia membros e gera convite.
    Restrições de permissão aplicadas conforme solicitado.
    """

    required_permission = 'editor'
    use_membership_filter = True

    def dispatch(self, request, *args, **kwargs):
        self.board = get_object_or_404(
            models.Board,
            slug=kwargs['slug'],
            created_by__username=kwargs['username']
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, username, slug):
        
        board_form = BoardForm(instance=self.board)
        members = models.BoardMember.objects.filter(board=self.board)
        invite_form = BoardInviteForm()

        context = {
            'board': self.board,
            'board_form': board_form,
            'members': members,
            'invite_form': invite_form,
        }
        return render(request, 'boards/board_edit.html', context)

    def post(self, request, username, slug):
        if 'save_board' in request.POST:
            board_form = BoardForm(request.POST, instance=self.board)
            members = models.BoardMember.objects.filter(board=self.board)
            invite_form = BoardInviteForm()
            if board_form.is_valid():
                board_form.save()
                messages.success(request, 'Board atualizado.')
                return redirect(reverse('board_edit', args=[username, slug]))

            context = {
                'board': self.board,
                'board_form': board_form,
                'members': members,
                'invite_form': invite_form,
            }
            return render(request, 'boards/board_edit.html', context)


class DeleteBoardView(LoginRequiredMixin, DeleteView):
    """
    Remove um board. Acesso restrito ao proprietário e apenas se for membro.
    """
    model = models.Board
    template_name = 'boards/board_delete.html'
    success_url = reverse_lazy('dashboard')

    required_permission = 'owner'
    use_membership_filter = True
        

    def get_object(self, queryset=None):
        return self.board

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        context['user_permission'] = 'owner'
        return context


class AddBoardMemberView(LoginRequiredMixin, CreateView):
    """
    Adiciona membro a um board.
    Apenas proprietários e moderadores podem adicionar membros.
    """
    model = models.BoardMember
    form_class = BoardMemberForm
    template_name = 'boards/add_members.html'

    required_permission = 'moderator'
    use_membership_filter = True  

    def form_valid(self, form):
        form.instance.board = self.board

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board

        board_member = self.board.memberships.get(
            member = self.request.user
        )
        user_permission = board_member.permission
        context['user_permission'] = user_permission

        allowed = {
            'owner': ['moderator', 'editor', 'viewer'],
            'moderator': ['editor', 'viewer']
        }.get(user_permission, [])

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

    required_permission = 'moderator'
    use_membership_filter = True

    def dispatch(self, request, username, slug, *args, **kwargs):
        try:
            self.board = models.Board.objects.get(slug=slug, created_by__username=username)
        except models.Board.DoesNotExist:
            return render(request, '404.html', status=404)  # Ou JsonResponse com status 404
        return super().dispatch(request, username, slug, *args, **kwargs)


    def get(self, request, username, slug):
        form = BoardInviteForm()
        return render(request, 'boards/invite_form.html', {'form': form, 'username': username, 'slug': slug})

    def post(self, request, username, slug):
        form = BoardInviteForm(request.POST)
        if form.is_valid():
            invite = models.BoardInvite.objects.create(
                board=self.board,
                invited_by=request.user,
                permission=form.cleaned_data['permission'],
                expires_at=timezone.now() + timedelta(days=7)
            )
            link = request.build_absolute_uri(
                reverse('board_invite_accept', args=[str(invite.token)])
            )
            return JsonResponse({
                "message": "Link de convite gerado com sucesso!",
                "link": link
            })
        return JsonResponse({
            "message": "Erro ao gerar convite. Verifique os dados do formulário."
        }, status=400)


class BoardInviteAcceptView(View):
    def get(self, request, token):
        invite = get_object_or_404(models.BoardInvite, token=token)

        if invite.accepted:
            messages.error(request, "Este convite já foi utilizado.")
            return redirect('dashboard')

        if not request.user.is_authenticated:
            request.session['pending_invite_token'] = str(token)
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

    required_permission = 'editor'
    use_membership_filter = True

    def dispatch(self, request, username, slug, *args, **kwargs):
        try:
            self.board = models.Board.objects.get(slug=slug, created_by__username=username)
        except models.Board.DoesNotExist:
            raise Http404("Board não encontrado")
        return super().dispatch(request, username, slug, *args, **kwargs)

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
    
    def post(self, request, username, slug, *args, **kwargs):
        # Se veio JSON, parseia e cria coluna direto
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
                name = data.get('name', '').strip()
                if not name:
                    return JsonResponse({'error': 'Nome inválido'}, status=400)

                self.board = models.Board.objects.get(slug=slug, created_by__username=username)

                # Verifica permissão do usuário para editar
                if not models.BoardMember.user_has_access(self.board, request.user, 'editor'):
                    return JsonResponse({'error': 'Permissão negada'}, status=403)

                column = models.Column.objects.create(board=self.board, name=name)
                return JsonResponse({'success': True, 'id': column.id, 'name': column.name})

            except models.Board.DoesNotExist:
                return JsonResponse({'error': 'Board não encontrado'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            # Caso normal de formulário, chama CreateView.post padrão
            return super().post(request, username, slug, *args, **kwargs)


class EditColumnAjaxView(LoginRequiredMixin, AjaxBoardPermissionMixin, View):
    required_permission = 'editor'  # Permissão necessária

    def post(self, request, username, slug, pk):
        try:
            column = models.Column.objects.get(pk=pk, board=self.board)
        except models.Column.DoesNotExist:
            return JsonResponse({'error': 'Coluna não encontrada'}, status=404)

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



class DeleteColumnAjaxView(LoginRequiredMixin, AjaxBoardPermissionMixin, View):
    required_permission = 'editor'  # ajusta para a permissão correta

    def post(self, request, username, slug, pk):
        try:
            column = models.Column.objects.get(pk=pk, board=self.board)
        except models.Column.DoesNotExist:
            return JsonResponse({'error': 'Coluna não encontrada'}, status=404)

        column.delete()
        return JsonResponse({'success': True})
