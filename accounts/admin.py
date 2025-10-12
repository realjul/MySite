from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# import CustomUser Creation and Change forms
from .forms import CustomUserCreationForm, CustomUserChangeForm
# set CustomUser to specific user, hence get_user_model()
CustomUser = get_user_model()
# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username","is_superuser"]

admin.site.register(CustomUser,CustomUserAdmin)