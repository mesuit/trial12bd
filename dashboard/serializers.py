from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Assignment, Withdrawal

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ["user", "balance", "referral_code", "is_verified", "referred_by"]

class AssignmentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Assignment
        fields = ["id", "title", "description", "type", "posted_by_admin", "owner", "files", "url", "text", "premium_only", "created_at"]

class CreateAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ["title", "description", "type", "files", "url", "text", "premium_only"]

class WithdrawalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Withdrawal
        fields = ["id", "user", "amount", "destination", "status", "requested_at", "processed_at"]
