from django.urls import path
from . import views


urlpatterns = [
    path('', views.BoardListView.as_view(), name='dashboard'),  # Lista boards do usuário logado
    path('novo/', views.BoardCreateView.as_view(), name='board_create'),

    # Ações relacionadas ao board
    path('<str:username>/<slug:slug>/', views.BoardDetailView.as_view(), name='board_detail'),
    path('<str:username>/<slug:slug>/edit/', views.BoardEditView.as_view(), name='board_edit'),

    # Colunas dentro do board
    path('<str:username>/<slug:slug>/add-column/', views.AddColumnView.as_view(), name='add_column'),
    path('<str:username>/<slug:slug>/columns/<int:pk>/edit-ajax/', views.EditColumnAjaxView.as_view(), name='column_edit_ajax'),
    path('<str:username>/<slug:slug>/columns/<int:pk>/delete-ajax/', views.DeleteColumnAjaxView.as_view(), name='column_delete_ajax'),

    # Tasks
    path('<str:username>/<slug:slug>/columns/<int:column_id>/add-task/', views.AddTaskAjaxView.as_view(), name='add_task'),
    path('<str:username>/<slug:slug>/columns/<int:column_id>/edit-task/<int:task_id>/', views.EditTaskAjaxView.as_view(), name='edit_task'),
    path('<str:username>/<slug:slug>/columns/<int:column_id>/delete-task/<int:task_id>/', views.TaskDeleteView.as_view(), name='delete_task'),

    # membros
    path('<str:username>/<slug:slug>/members/', views.BoardManageMembersView.as_view(), name='board_manage_members'),
    path('<str:username>/<slug:slug>/invite/<uuid:token>/', views.BoardInviteAcceptView.as_view(), name='board_invite_accept'),
    

]
