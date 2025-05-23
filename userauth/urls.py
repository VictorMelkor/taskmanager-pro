from django.urls import path
from . import views

app_name = 'userauth'  # ESSENCIAL para registrar o namespace

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
]
