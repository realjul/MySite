from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from jobs.models import Profile, EmployeeJob

User = get_user_model()

# Create your models here.
class ScheduleDay(models.Model):
    date = models.DateField(unique=True)
    projected_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(Profile,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   related_name='created_schedules'
                                   )
    def __str__(self):
        return f"Schedule for {self.date}"


"""

schedule_day.created_by = request.user.profile
"""
class Shift(models.Model):
    SHIFT_CHOICES = (
        ('AM','Morning'),
        ('MID','Mid'),
        ('PM','Evening'),
    )
    day = models.ForeignKey(ScheduleDay, on_delete=models.CASCADE, related_name='shifts')
    employee_job = models.ForeignKey(EmployeeJob, on_delete=models.SET_NULL, null=True)

    shift_type = models.CharField(max_length=4, choices=SHIFT_CHOICES,blank=True)
    section_number = models.PositiveIntegerField(null=True, blank=True)

    start_time = models.TimeField(null=True, blank=False)
    end_time = models.TimeField(null=True, blank=False)

    def __str__(self):
        return f"{self.employee_job.profile.user.username} - {self.shift_type} ({self.day.date})"

    @property
    def hours(self):
        """
        Automatically calculate the number of hours based on start/end time.
        Handles shifts that pass midnight.
        """
        start = timezone.datetime.combine(self.day.date, self.start_time)
        end = timezone.datetime.combine(self.day.date, self.end_time)

        # Handle overnight shift (example: 10 PM to 2 AM)
        if end < start:
            end += timezone.timedelta(days=1)

        delta = end - start
        return round(delta.total_seconds() / 3600, 2)


