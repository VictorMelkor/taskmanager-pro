from django.contrib import admin
from django.urls import path, include
from userauth import views as userauth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home e dashboard vêm de pages
    path('', include(('pages.urls', 'pages'), namespace='pages')),

    # Rotas de tarefas
    path('tasks/', include('tasks.urls')),

    # Cadastro e logout personalizados direto nas views
    path('signup/', userauth_views.signup_view, name='signup'),
    path('logout/', userauth_views.custom_logout, name='custom_logout'),

    # Login via userauth app (login personalizado)
    path('auth/', include(('userauth.urls', 'userauth'), namespace='userauth')),

    # Allauth URLs padrão para social, reset, etc.
    path('accounts/', include('allauth.urls')),
]
