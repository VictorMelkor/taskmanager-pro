from django.urls import path
from . import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name='dashboard'),  # Lista boards do usuário logado
    
    # Corrigido para o nome correto da view de criação de board
    path('novo/', views.BoardCreateView.as_view(), name='board_create'),  

    # Invite: usar apenas CreateBoardInviteView para criar convite
    path('<str:username>/<slug:slug>/invite/', views.CreateBoardInviteView.as_view(), name='create_board_invite'),
    path('invite/accept/<uuid:token>/', views.BoardInviteAcceptView.as_view(), name='board_invite_accept'),


    # Removi AddBoardMemberView e InviteCreateView por estarem duplicadas ou não usadas
    # path('<str:username>/<slug:slug>/add-member/', views.AddBoardMemberView.as_view(), name='add_board_member'),
    # path('boards/<username>/<slug>/invite/', views.InviteCreateView.as_view(), name='invite'),

    path('<str:username>/<slug:slug>/update/', views.UpdateBoardView.as_view(), name='board_update'),
    path('<str:username>/<slug:slug>/edit/', views.BoardEditView.as_view(), name='board_edit'),
    path('<str:username>/<slug:slug>/delete/', views.DeleteBoardView.as_view(), name='board_delete'),
    path('<str:username>/<slug:slug>/', views.BoardDetailView.as_view(), name='board_detail'),
    path('<str:username>/<slug:slug>/add-column/', views.AddColumnView.as_view(), name='add_column'),
    path('<str:username>/<slug:slug>/columns/<int:pk>/edit-ajax/', views.EditColumnAjaxView.as_view(), name='column_edit_ajax'),
    path('<str:username>/<slug:slug>/columns/<int:pk>/delete-ajax/', views.DeleteColumnAjaxView.as_view(), name='column_delete_ajax'),
]
