from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CQUserChangeForm, CQUserCreationForm
from .models import CQUser, MemberProfile


class CQUserAdmin(UserAdmin):
    add_form = CQUserCreationForm
    form = CQUserChangeForm
    model = CQUser
    list_display = (
        "trigram",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "trigram",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("trigram", "email", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "trigram",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = (
        "email",
        "trigram",
    )
    ordering = ("trigram",)


admin.site.register(CQUser, CQUserAdmin)


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "updated_at", "avatar"]
    raw_id_fields = ["user"]
