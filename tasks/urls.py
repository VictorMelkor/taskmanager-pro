from django.urls import path
from . import views

app_name = 'tasks'  # Namespace do app

urlpatterns = [
    # Página que exibe um board específico (com colunas e tarefas)
    path('board/<int:board_id>/', views.board_view, name='board'),

    # Página para criar um novo board
    path('board/create/', views.create_board, name='create_board'),

    # Adicionar tarefa via POST (não está usando board_id, mas poderia)
    path('task/add/', views.task_add, name='task_add'),

    # Adicionar tarefa em uma coluna específica (com board_id para segurança)
    path('board/<int:board_id>/add_task/<int:column_id>/', views.add_task, name='add_task'),
]
