from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    referral_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    referred_by = models.CharField(max_length=50, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="assignments/", blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    created_at = models.DateTimeField(auto_now_add=True)
