from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView, FormView
from django.urls import reverse, reverse_lazy
from django.http import Http404, JsonResponse, HttpResponseForbidden, HttpResponse
from django.utils.text import slugify
from django.utils import timezone
from django.views import View
from datetime import timedelta
import json
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models


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


class BoardEditView(LoginRequiredMixin, BoardPermissionRequiredMixin, View):
    """
    Edita board, gerencia membros, convites e exclusão.
    """

    required_permission = 'editor'
    use_membership_filter = True

    # Não sobrescreve dispatch, deixa o mixin cuidar da permissão e carregar self.board

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
        # Exclusão só para owner
        if 'delete_board' in request.POST:
            if self.board.created_by != request.user:
                return HttpResponseForbidden("Você não tem permissão para excluir este board.")
            self.board.delete()
            messages.success(request, 'Board excluído com sucesso.')
            return redirect('dashboard')

        # Salvar alterações
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

        # POST inesperado - renderiza com formulário vazio
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




class BoardManageMembersView(LoginRequiredMixin, BoardPermissionRequiredMixin, View):
    required_permission = 'moderator'
    use_membership_filter = True

    def get(self, request, username, slug):
        self.membership = self.board.memberships.get(member=request.user)
        invite_form = BoardInviteForm()
        members = self.board.memberships.select_related('member')

        invite_link = request.session.pop('invite_link', None)

        context = {
            'board': self.board,
            'members': members,
            'invite_form': invite_form,
            'user_permission': self.membership.permission,
            'invite_link': invite_link,
        }
        return render(request, 'boards/board_manage_members.html', context)

    def post(self, request, username, slug):
        self.membership = self.board.memberships.get(member=request.user)

        if 'remove_member' in request.POST:
            member_id = request.POST.get('remove_member')
            member = get_object_or_404(models.BoardMember, pk=member_id, board=self.board)

            if member.member == request.user:
                messages.error(request, "Você não pode se remover do quadro.")
            elif member.permission == 'owner':
                messages.error(request, "Você não pode remover o proprietário do quadro.")
            else:
                member.delete()
                messages.success(request, "Membro removido com sucesso.")

            return redirect('board_manage_members', username=username, slug=slug)

        invite_form = BoardInviteForm(request.POST)
        if invite_form.is_valid():
            invite = models.BoardInvite.objects.create(
                board=self.board,
                invited_by=request.user,
                permission=invite_form.cleaned_data['permission'],
                expires_at=timezone.now() + timedelta(days=7)
            )
            invite_link = request.build_absolute_uri(
                reverse('board_invite_accept', args=[self.board.created_by.username, self.board.slug, str(invite.token)])
            )
            request.session['invite_link'] = invite_link
            messages.success(request, "Convite gerado com sucesso.")

            return redirect('board_manage_members', username=username, slug=slug)

        members = self.board.memberships.select_related('member')
        context = {
            'board': self.board,
            'members': members,
            'user_permission': self.membership.permission,
            'invite_form': invite_form,
        }
        return render(request, 'boards/board_manage_members.html', context)




class BoardInviteAcceptView(View):
    def get(self, request, username, slug, token):
        # 1. Buscar o board
        board = get_object_or_404(models.Board, slug=slug, created_by__username=username)

        # 2. Buscar convite válido pelo token
        invite = get_object_or_404(models.BoardInvite, token=token)

        # 3. Validar que o convite pertence ao board correto
        if invite.board != board:
            messages.error(request, "Este convite não pertence ao quadro especificado.")
            return redirect('dashboard')

        # 4. Verificar se o convite está expirado
        if invite.expires_at and invite.expires_at < timezone.now():
            messages.error(request, "Este convite expirou.")
            return redirect('dashboard')

        # 5. Verificar se usuário está autenticado
        if not request.user.is_authenticated:
            messages.info(request, "Faça login para aceitar o convite.")
            return redirect('login')  # Ajuste a URL de login se necessário

        # 6. Verificar se já é membro
        membership_exists = board.memberships.filter(member=request.user).exists()
        if membership_exists:
            messages.info(request, "Você já é membro deste quadro.")
            return redirect('board_detail', username=username, slug=slug)  # Ajuste essa URL

        # 7. Criar vínculo de membro
        models.BoardMember.objects.create(
            board=board,
            member=request.user,
            permission=invite.permission
        )

        # Opcional: invalidar o convite para evitar reutilização
        invite.delete()

        messages.success(request, "Você entrou no quadro com sucesso!")
        return redirect('board_detail', username=username, slug=slug)




class AddColumnView(LoginRequiredMixin, View):
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
                return JsonResponse({
                    'success': True, 
                    'id': column.id, 
                    'name': column.name,
                    'add_task_url': f'/dashboard/{username}/{slug}/columns/{column.id}/add-task/',
                    })

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
    

class AddTaskAjaxView(LoginRequiredMixin, AjaxBoardPermissionMixin, CreateView):
    model = models.Task
    fields = ['name', 'description', 'status']
    template_name = 'boards/add_task.html'

    required_permission = 'editor'
    use_membership_filter = True 

    def dispatch(self, request, *args, **kwargs):
        username = kwargs.get('username')
        slug = kwargs.get('slug')
        column_id = kwargs.get('column_id')
        try:
            self.board = models.Board.objects.get(slug=slug, created_by__username=username)
            self.column = models.Column.objects.get(id=column_id, board=self.board)
        except (models.Board.DoesNotExist, models.Column.DoesNotExist):
            raise Http404("Quadro ou Coluna não encontrada")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.column = self.column
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['column'] = self.column
        return context

    def get_success_url(self):
        return reverse('board_detail', kwargs={
            'username': self.kwargs.get('username'),
            'slug': self.kwargs.get('slug')
        })

    def post(self, request, *args, **kwargs):
        username = kwargs.get('username')
        slug = kwargs.get('slug')
        column_id = kwargs.get('column_id')

        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
                name = data.get('name', '').strip()
                if not name:
                    return JsonResponse({'error': 'Nome inválido'}, status=400)

                # Permissão
                if not models.BoardMember.user_has_access(self.board, request.user, 'editor'):
                    return JsonResponse({'error': 'Permissão negada'}, status=403)

                task = models.Task.objects.create(column=self.column, name=name, created_by=request.user)
                return JsonResponse({
                    'success': True, 
                    'id': task.id, 
                    'name': task.name, 
                    'status': task.status, 
                    'created_at': task.created_at.isoformat()
                })

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return super().post(request, *args, **kwargs)


class EditTaskAjaxView(LoginRequiredMixin, AjaxBoardPermissionMixin, UpdateView):
    required_permission = 'editor'
    model = models.Task
    fields = ['name', 'description', 'status']

    def dispatch(self, request, *args, **kwargs):
        self.board = get_object_or_404(models.Board, slug=kwargs['slug'], created_by__username=kwargs['username'])
        self.column = get_object_or_404(models.Column, id=kwargs['column_id'], board=self.board)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(models.Task, id=self.kwargs['task_id'], column=self.column)

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({
            'success': True,
            'id': self.object.id,
            'name': self.object.name,
            'description': self.object.description,
            'status': self.object.status,
        }, status=200)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except:
            data = request.POST
        form_class = self.get_form_class()
        form = form_class(data, instance=self.get_object())
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
    
class TaskDeleteView(AjaxBoardPermissionMixin, View):
    required_permission = 'editor'

    def post(self, request, username, slug, column_id, task_id, *args, **kwargs):
        try:
            task = models.Task.objects.get(
                id=task_id,
                column_id=column_id,
                column__board=self.board
            )
            task.delete()
            return JsonResponse({'success': True})
        except models.Task.DoesNotExist:
            return JsonResponse({'error': 'Tarefa não encontrada'}, status=404)