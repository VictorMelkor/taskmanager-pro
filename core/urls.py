from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rotas do app pages
    path('', include(('pages.urls', 'pages'), namespace='pages')),

    # Rotas do app tasks
    path('tasks/', include(('tasks.urls', 'tasks'), namespace='tasks')),

    # Rotas de autenticação personalizadas e allauth
    path('userauth/', include(('userauth.urls', 'userauth'), namespace='userauth')),

    # Ou pode usar diretamente as views de userauth, se quiser (exemplo abaixo)

    # path('signup/', userauth_views.signup_view, name='signup'),
    # path('logout/', userauth_views.custom_logout, name='custom_logout'),

    # Incluindo todas as urls do allauth
    path('accounts/', include('allauth.urls')),
]
