from django.urls import path

from .forms import ProfileUpdateForm
from .views import SignupPageView, ProfileDetailView, ProfileUpdateView, UploadPDFsView

urlpatterns = [
    path("signup/", SignupPageView.as_view(), name="signup"),
path("profile/edit/", ProfileUpdateView.as_view(), name="profile-edit"),
    path("profile/<str:email>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("upload_pdfs/", UploadPDFsView.as_view(), name="upload_pdfs"),

]