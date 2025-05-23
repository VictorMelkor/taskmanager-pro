from django.urls import path
from .views import home_view, dashboard

app_name = 'pages'

urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
]
