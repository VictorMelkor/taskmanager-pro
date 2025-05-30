from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, email, full_name=None, password=None, **extra_fields):
        """
        Cria e salva um usuário regular com username, email e senha.
        - username e email são obrigatórios.
        - full_name é opcional.
        - Se password não for fornecida, cria um usuário sem senha (não pode logar por senha).
        """
        if not username:
            raise ValueError('O username é obrigatório')
        if not email:
            raise ValueError('O email é obrigatório')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, full_name=full_name, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, full_name=None, password=None, **extra_fields):
        """
        Cria e salva um superusuário com permissões administrativas.
        - Garante que is_staff, is_superuser e is_active estejam True.
        - Repassa a criação para create_user.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')

        return self.create_user(username, email, full_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=150, blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """Retorna o username como representação do objeto."""
        return self.username
    
    def get_full_name(self):
        """Retorna o nome completo, ou username se o nome completo não existir."""
        return self.full_name or self.username
    
    def get_short_name(self):
        """Retorna o username como nome curto."""
        return self.username
