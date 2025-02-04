

"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
# _  A shortcut for translating text in different languages.

from core import models


class UserAdmin(BaseUserAdmin):  # manages the display of users in admin
    """Define the admin pages for users"""

    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
             _('Permissions'),
             {
                 'fields': (
                     'is_active',
                     'is_staff',
                     'is_superuser',
                 )
             }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # classes makes page neater
            'fields': (
                        'email',
                        'password1',
                        'password2',
                        'name',
                        'is_active',
                        'is_staff',
                        'is_superuser',
             )
        }),
    )


# registers your custom User model with the UserAdmin
# to use your UserAdmin class when displaying
# and managing users in the admin
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
