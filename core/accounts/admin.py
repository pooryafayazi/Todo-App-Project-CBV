from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

# Register your models here.




class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ['id']
    list_display = ['id','email', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['email','is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        ('Authentications', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('group permissions', {'fields': ('groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_active', 'is_staff', 'is_superuser')
        }),
    )
class CustomProfileAdmin(admin.ModelAdmin):
    model = Profile
    ordering = ['id']
    list_display = ['id','user', 'first_name', 'last_name']
    list_filter = ['user']
    searching_fields = ['id','user', 'first_name', 'last_name']
    


admin.site.register(Profile, CustomProfileAdmin) 
admin.site.register(User, CustomUserAdmin)