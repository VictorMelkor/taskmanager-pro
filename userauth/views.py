from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import UserCreationForm, CustomAuthenticationForm

class CustomLoginView(LoginView):
    template_name = 'userauth/login.html'
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm 

    
    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('dashboard')




def signup(request):
    """
    View para o cadastro de novos usuários.
    GET: exibe formulário em branco.
    POST: valida dados, cria usuário, realiza login automático e redireciona para 'dashboard'.
    Se inválido, reexibe formulário com erros.
    """
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'userauth/signup.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            token = request.session.pop('pending_invite_token', None)
            if token:
                return redirect('board_invite_accept', token=token)
            return redirect('dashboard')
        else:
            return render(request, 'userauth/signup.html', {'form': form})
        
class CustomLogoutView(LogoutView):
    """
    View para logout.
    Após logout, redireciona para a URL nomeada 'home'.
    """
    next_page = reverse_lazy('home')
