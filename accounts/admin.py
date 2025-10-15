from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . models import User , UserProfile
# Register your models here.


class UserAdmin(BaseUserAdmin):
    list_display= ('email','username', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


    fieldsets = (
        (None,{'fields': ('email', 'full_name', 'password')}),
        ('permission', {'fields':('is_admin', 'is_superuser','is_active','groups','user_permissions')}),
    )

    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields': ('email', 'full_name','password1', 'password2', 'is_admin','is_superuser','is_active')
        }),
    )

    search_fields = (
        'email', 'full_name'
    )
    ordering = ('email',)

    filter_horizontal = ('groups','user_permissions',)

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
