from django import forms
from .models import JobBase, EmployeeJob

class JobBaseForm(forms.ModelForm):
    class Meta:
        model = JobBase
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'department': forms.Select(attrs={'class':'form-control'}),
        }
class EmployeeJobForm(forms.ModelForm):
    class Meta:
        model = EmployeeJob
        fields = '__all__'
        widgets = {
            'profile': forms.Select(attrs={'class':'form-select'}),
            'job': forms.Select(attrs={'class':'form-select'}),
            'start_date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class':'form-check-input'}),

        }
