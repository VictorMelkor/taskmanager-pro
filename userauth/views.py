from django.shortcuts import render, redirect
from allauth.account.forms import SignupForm, LoginForm
from django.contrib import messages
from django.contrib.auth import logout, login
from allauth.account.utils import perform_login


from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso! Bem-vindo(a)!')
            return redirect('pages:dashboard')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = SignupForm()
    return render(request, 'userauth/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.user
            perform_login(request, user, email_verification='optional')
            return redirect('pages:dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos. Tente novamente.')
    else:
        form = LoginForm(request=request)
    return render(request, 'userauth/login.html', {'form': form})



def custom_logout(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta.")
    return redirect('pages:home')
