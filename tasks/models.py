from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Board(models.Model):
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default="#ffffff")  # nova cor
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Column(models.Model):
    title = models.CharField(max_length=100)
    board = models.ForeignKey(Board, related_name='columns', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'A Fazer'),
        ('doing', 'Em Andamento'),
        ('done', 'Concluída'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    column = models.ForeignKey(Column, related_name='tasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    responsible = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')

    def __str__(self):
        return self.title
