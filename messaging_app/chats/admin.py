from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Conversation, Message
from django.utils.translation import gettext_lazy as _


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "bio",
                    "profile_picture",
                    "phone_number",
                )
            },
        ),
        # (
        #     _("Permissions"),
        #     {
        #         "fields": (
        #             "is_active",
        #             "is_staff",
        #             "is_superuser",
        #             "groups",
        #             "user_permissions",
        #         )
        #     },
        # ),
        # (_("Important dates"), {"fields": ("last_login", "date_joined", "last_seen")}),
        (_("Status"), {"fields": ("is_online",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    list_display = ("user_id", "username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


admin.site.register(Conversation)
admin.site.register(Message)
