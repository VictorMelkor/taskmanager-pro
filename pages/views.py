from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tasks.models import Board

def home_view(request):
    return render(request, 'pages/home.html')

@login_required
def dashboard(request):
    boards = Board.objects.filter(owner=request.user)
    return render(request, 'pages/dashboard.html', {'boards': boards})
