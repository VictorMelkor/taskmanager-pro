from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(DjangoUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    #readonly_fields = ('last_login', 'date_joined', 'two_factor_enabled', 'two_factor_info')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'full_name')}), 
        ('Permissões', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
        ('Segurança', {'fields': ('two_factor_enabled', 'two_factor_info')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'email', 'full_name', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username', )

admin.site.register(User, UserAdmin)
