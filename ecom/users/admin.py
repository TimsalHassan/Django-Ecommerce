from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
admin.site.register(Profile)


# Mix Profile info and User Info
class ProfileInline(admin.StackedInline):
    model = Profile
    on_delete = False
    verbose_name_plural = Profile


# Extend User admin
class CustomUserAdmin(BaseUserAdmin):
    # model = User
    # fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

# Unregister the Old Way
admin.site.unregister(User)

# Re-Register the New Way
admin.site.register(User, CustomUserAdmin)
