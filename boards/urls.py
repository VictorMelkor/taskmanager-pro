from django.urls import path
from . import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name='dashboard'),  # Lista boards do usuário logado
    path('novo/', views.BoardCreateView.as_view(), name='board_create'),

    # Ações relacionadas ao board
    path('<str:username>/<slug:slug>/', views.BoardDetailView.as_view(), name='board_detail'),
    path('<str:username>/<slug:slug>/edit/', views.BoardEditView.as_view(), name='board_edit'),
    path('<str:username>/<slug:slug>/delete/', views.DeleteBoardView.as_view(), name='board_delete'),

    # Colunas dentro do board
    path('<str:username>/<slug:slug>/add-column/', views.AddColumnView.as_view(), name='add_column'),
    path('<str:username>/<slug:slug>/columns/<int:pk>/edit-ajax/', views.EditColumnAjaxView.as_view(), name='column_edit_ajax'),
    path('<str:username>/<slug:slug>/columns/<int:pk>/delete-ajax/', views.DeleteColumnAjaxView.as_view(), name='column_delete_ajax'),

    # Convites
    path('<str:username>/<slug:slug>/invite/', views.CreateBoardInviteView.as_view(), name='create_board_invite'),
    path('invite/accept/<uuid:token>/', views.BoardInviteAcceptView.as_view(), name='board_invite_accept'),
]
