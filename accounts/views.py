from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

# created when creating abstractuser
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Profile


# Create your views here.
class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "account/signup.html"

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profile.html"
    context_object_name = "profile"
    def get_object(self):
        email = self.kwargs.get("email")
        return get_object_or_404(Profile, user__email=email)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user.profile

    def test_func(self):
        return self.get_object().user == self.request.user
