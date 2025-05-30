from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, UserChangeForm as DjangoUserChangeForm
from .models import User

class UserCreationForm(DjangoUserCreationForm):
    """
    Formulário para criação de usuário baseado no modelo customizado User.
    Campos incluídos: username e email.
    """
    class Meta:
        model = User
        fields = ('username', 'email')

class UserChangeForm(DjangoUserChangeForm):
    """
    Formulário para edição de usuário baseado no modelo customizado User.
    Campos incluídos: username, email e full_name.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'full_name')
