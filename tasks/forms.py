from django import forms

COLOR_CHOICES = [
    ('#FF6B6B', 'Vermelho'),
    ('#4ECDC4', 'Verde Água'),
    ('#556270', 'Cinza Azulado'),
    ('#C7F464', 'Amarelo Limão'),
    ('#FFA500', 'Laranja'),
]

class BoardForm(forms.Form):
    title = forms.CharField(label='Título do Board', max_length=100)
    color = forms.ChoiceField(label='Cor do Board', choices=COLOR_CHOICES, widget=forms.RadioSelect)
