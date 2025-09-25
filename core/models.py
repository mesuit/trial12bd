from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

def generate_referral():
    return str(uuid.uuid4())[:8]  # short unique code

class User(AbstractUser):
    referral_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    referred_by = models.CharField(max_length=50, blank=True, null=True)  # stores referral code of inviter
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_verified = models.BooleanField(default=False)  # track premium/paid users

    def save(self, *args, **kwargs):
        # auto-generate referral_code if empty
        if not self.referral_code:
            self.referral_code = generate_referral()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="assignments/", blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (by {self.submitted_by.username})"
