# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, ApplicationProfile

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ("email", "username", "is_staff", "is_active",)
    list_filter = ("email", "username", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "username", "password",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email","username", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register([ApplicationProfile])
admin.site.register(User, UserAdmin)