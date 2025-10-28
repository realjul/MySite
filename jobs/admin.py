from django.contrib import admin
from .models import JobBase, EmployeeJob

# Register your models here.
admin.site.register(JobBase)
admin.site.register(EmployeeJob)

