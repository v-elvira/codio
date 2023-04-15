from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from codio_auth.models import User
from django.utils.translation import gettext_lazy as _

class CodioUserAdmin(UserAdmin): # https://github.com/django/django/blob/2978c63a34b4aa0f170a1e5a0f8f4cb2811fa248/django/contrib/auth/admin.py#L41
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(User, CodioUserAdmin)
