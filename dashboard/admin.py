from django.contrib import admin
from .models import Profile, Assignment, Withdrawal

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "referral_code", "is_verified")

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "posted_by_admin", "owner", "premium_only", "created_at")

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "status", "requested_at")
