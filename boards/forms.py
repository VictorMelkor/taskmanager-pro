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
        widgets = {
            'description': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input-field'})

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input-field'})