from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Location

# import CustomUser Creation and Change forms
from .forms import CustomUserCreationForm, CustomUserChangeForm
# set CustomUser to specific user, hence get_user_model()
CustomUser = get_user_model()
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    fields = ("image","phone","location","shirt_size")

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username","is_superuser"]



admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Location)
admin.site.register(Profile)