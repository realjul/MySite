from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    SHIRT_SIZES = (
        ("XS","Extra Small"),
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "Extra Large"),
        ("XXL", "Extra XLarge"),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=10,default="0000000000")
    image = models.ImageField(upload_to="covers/", blank=True, null=True, default=None)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="location")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="profile")
    shirt_size = models.CharField(max_length=15,
                                  choices=SHIRT_SIZES,
                                  blank=True,
                                  null=True)

    def primary_job(self):
        """Return the employee's primary job if one is set"""
        return self.employee_jobs.filter(is_primary=True).first()

    def __str__(self):
        return f"{self.user.username}'s"