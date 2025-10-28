from django.db import models
from accounts.models import Profile
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
# ---- Base jobs class -----
class JobBase(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.title


class EmployeeJob(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="employee_jobs"
    )
    job = models.ForeignKey(
        JobBase, on_delete=models.CASCADE, related_name="employees"
    )
    start_date = models.DateField(auto_now_add=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ('profile', 'job')

    def __str__(self):
        return f"{self.profile.user.username} - {self.job.title}"