from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid
from datetime import timedelta
from django.utils import timezone


class Board(models.Model):
    COLOR_CHOICES = [
        ('theme1', 'Degradê Laranja'),
        ('theme2', 'Degradê Azul'),
        ('theme3', 'Degradê Verde'),
        ('theme4', 'Degradê Rosa'),
    ]

    IMAGE_CHOICES = [
        ('none', 'Nenhuma'),
        ('img1', 'Imagem 1'),
        ('img2', 'Imagem 2'),
        ('img3', 'Imagem 3'),
    ]

    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="boards")
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    show_calendar = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=False)
    color_theme = models.CharField(max_length=50, choices=COLOR_CHOICES, blank=True, null=True, default='theme2')
    background_image = models.CharField(max_length=10, choices=IMAGE_CHOICES, default='none')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            while Board.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class BoardMember(models.Model):
    """
    Relaciona usuários a boards com níveis de permissão.
    """
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="board_memberships")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="memberships" )

    PERMISSION_CHOICES = [
        ('owner', 'Proprietário'),
        ('moderator', 'moderador'),
        ('editor', 'Editor'),
        ('viewer', 'Leitor'),
    ]

    permission = models.CharField(max_length=12, choices=PERMISSION_CHOICES, default='viewer')

    class Meta:
        unique_together = ('board', 'member')

    def __str__(self):
        """
        Retorna string indicando o membro, board e sua permissão.
        """
        return f"{self.member} em {self.board} ({self.permission})"
    
    @staticmethod
    def user_has_access(board, user, min_permission=None):
        """
        Verifica se o usuário tem acesso ao board.
        Se min_permission for passado, verifica se o nível do usuário é igual ou superior.
        """
        member = BoardMember.objects.filter(board=board, member=user).first()
        if not member:
            return False

        if not min_permission:
            return True

        # Define ordem hierárquica das permissões
        hierarchy = ['viewer', 'editor', 'moderator', 'owner']
        user_level = hierarchy.index(member.permission)
        required_level = hierarchy.index(min_permission)

        return user_level >= required_level

    @staticmethod
    def get_user_permission(board, user):
        """
        Retorna a permissão do usuário no board, ou None.
        """
        member = BoardMember.objects.filter(board=board, member=user).first()
        return member.permission if member else None
    
    def has_permission(self, *allowed_roles):
        return self.permission in allowed_roles
    

User = get_user_model()

class BoardInvite(models.Model):
    """
    Convite para usuário entrar em um board via token único e expiração.
    """
    PERMISSION_CHOICES = [
        ('viewer', 'Visualizador'),
        ('editor', 'Editor'),
        ('moderator', 'Moderador'),
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    def is_expired(self):
        return timezone.now() > self.expires_at



class Column(models.Model):
    """
    Colunas dentro de um board para organizar tarefas.
    """
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Task(models.Model):
    """
    Tarefas associadas a colunas com status e ordenação.
    """
    STATUS_CHOICES = [
        ('todo', 'Pendente'),
        ('doing', 'Em andamento'),
        ('done', 'Concluído'),
    ]

    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
