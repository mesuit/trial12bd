from django.db import models
from django.contrib.auth.models import User
import uuid

def user_referral_code():
    return uuid.uuid4().hex[:8]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    referral_code = models.CharField(max_length=50, unique=True, default=user_referral_code)
    referred_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="referrals")
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Assignment(models.Model):
    TYPE_CHOICES = (("local","Local"), ("international","International"))
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="local")
    posted_by_admin = models.BooleanField(default=False)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="submitted_assignments")
    files = models.FileField(upload_to="assignments/", null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    premium_only = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Withdrawal(models.Model):
    STATUS = (("Pending","Pending"), ("Approved","Approved"), ("Rejected","Rejected"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="withdrawals")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    destination = models.CharField(max_length=255, blank=True)  # e.g. mpesa phone or paypal
    status = models.CharField(max_length=20, choices=STATUS, default="Pending")
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.status})"
