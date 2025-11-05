from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Profile, ProfilePDF

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email","username")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("email","username")

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone','location','shirt_size','image','emergency_contact','emergency_contact_number')

class ProfilePDFForm(forms.ModelForm):
    class Meta:
        model = ProfilePDF
        fields = ['title','file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and not file.name.lower().endswith('.pdf'):
            raise forms.ValidationError('File must be an PDF')
        return file
