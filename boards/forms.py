from django import forms
from .models import BoardMember, Board, BoardInvite


class BoardMemberForm(forms.ModelForm):
    """
    Formulário para adicionar um membro a um board.
    """
    class Meta:
        model = BoardMember
        fields = ['member', 'permission']


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description', 'color_theme']

class BoardInviteForm(forms.Form):
    PERMISSION_CHOICES = [
        ('moderator', 'Moderador'),
        ('editor', 'Editor'),
        ('viewer', 'Visualizador'),
    ]
    permission = forms.ChoiceField(
        choices=PERMISSION_CHOICES, 
        label='Permissão', 
        initial='viewer')