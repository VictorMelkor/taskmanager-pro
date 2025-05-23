from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Column, Task
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import BoardForm

def board_view(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    columns = Column.objects.all().prefetch_related('tasks')
    return render(request, 'tasks/board.html', {'columns': columns})

@login_required
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            # Salva o board com dados do usuário logado
            Board.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                color=form.cleaned_data['color']
            )
            return redirect('pages:dashboard')  # ou a url que leva ao dashboard
    else:
        form = BoardForm()

    return render(request, 'tasks/create_board.html', {'form': form})

def add_task(request, board_id, column_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        column = get_object_or_404(Column, id=column_id, board__id=board_id, board__owner=request.user)
        Task.objects.create(title=title, description=description, column=column)
    return redirect('tasks:board', board_id=board_id)

@require_POST
def task_add(request):
    title = request.POST.get('title')
    status = request.POST.get('status')
    if title and status:
        Task.objects.create(title=title, status=status)
    return redirect('board')  # Corrigido
