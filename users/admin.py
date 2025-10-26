from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'dni', 'role', 'is_active']
    list_filter = ['role', 'biological_sex', 'is_active', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Personal', {'fields': ('dni', 'biological_sex', 'date_of_birth', 'phone')}),
        ('Rol', {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información Personal', {'fields': ('first_name', 'last_name', 'dni', 'biological_sex', 'date_of_birth', 'phone')}),
        ('Rol', {'fields': ('role',)}),
    )
