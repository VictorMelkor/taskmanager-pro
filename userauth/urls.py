from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, CustomLoginView, CustomLogoutView

urlpatterns = [
    path('signup/', signup, name='signup'),  
    # URL para cadastro de usuário

    path('login/', CustomLoginView.as_view(), name='login'),  
    # URL para login customizado usando CustomLoginView

    path('logout/', CustomLogoutView.as_view(), name='logout')  
    # URL para logout usando CustomLogoutView
]
