from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from .forms import AccountChangeForm, AccountCreateForm


# Register your models here.


@admin.register(Account)
class AccountAdmin(UserAdmin):
    add_form = AccountCreateForm
    form = AccountChangeForm
    model = Account

    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'last_login',)
    list_display_links = ('email', 'first_name',)
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('-email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

# admin.site.register(Account, AccountAdmin)
