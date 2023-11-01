from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Individual Data',
            {
                'fields':
                    (
                        'custom', 'phone', 'address'
                    )
            }
        )
    )

    list_display = [
        "username",
        "first_name",
        "last_name",
        "phone",
        "address"
    ]

    fields = (
        "email",
        "password"
    )
