from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('userauth.urls')),
    path('', include('pages.urls')),
    path('dashboard/', include('boards.urls')),
    
]
