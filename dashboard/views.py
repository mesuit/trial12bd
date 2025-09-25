from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile, Assignment, Withdrawal
from .serializers import ProfileSerializer, AssignmentSerializer, CreateAssignmentSerializer, WithdrawalSerializer
from rest_framework.parsers import MultiPartParser, FormParser

# Helper: create tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "token": str(refresh.access_token)}

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")
    referral = request.data.get("referral") or request.data.get("ref")

    if not name or not email or not password:
        return Response({"error": "name, email, password required"}, status=400)

    if User.objects.filter(username=name).exists():
        return Response({"error": "username taken"}, status=400)
    if User.objects.filter(email=email).exists():
        return Response({"error": "email taken"}, status=400)

    user = User.objects.create_user(username=name, email=email, password=password)
    profile = Profile.objects.create(user=user)

    # handle referral
    if referral:
        try:
            ref_profile = Profile.objects.get(referral_code=referral)
            profile.referred_by = ref_profile.user
            profile.save()
            # reward referrer: simple + to referrer balance
            ref_profile.balance += 5
            ref_profile.save()
        except Profile.DoesNotExist:
            pass

    tokens = get_tokens_for_user(user)
    return Response(tokens)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    # the frontend posts {email, password} or {username, password}
    email_or_username = request.data.get("email") or request.data.get("username")
    password = request.data.get("password")
    if not email_or_username or not password:
        return Response({"error": "credentials required"}, status=400)

    # try find by email
    try:
        user = User.objects.get(email=email_or_username)
        username = user.username
    except User.DoesNotExist:
        username = email_or_username

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "invalid credentials"}, status=400)

    tokens = get_tokens_for_user(user)
    return Response(tokens)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile)
    # include assignments visible to user
    assignments = Assignment.objects.filter(premium_only=False) | Assignment.objects.filter(premium_only=True, owner=request.user)
    assign_ser = AssignmentSerializer(assignments.order_by("-created_at"), many=True)
    data = serializer.data
    data["assignments"] = assign_ser.data
    return Response(data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_referral(request):
    profile = Profile.objects.get(user=request.user)
    link = request.build_absolute_uri("/") + f"?ref={profile.referral_code}"
    return Response({"referralCode": profile.referral_code, "link": link})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def submit_assignment(request):
    # accepts files (one), url, text, type
    data = request.data
    serializer = CreateAssignmentSerializer(data=data)
    if serializer.is_valid():
        assignment = serializer.save(owner=request.user, posted_by_admin=False)
        return Response(AssignmentSerializer(assignment).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def withdraw(request):
    amount = request.data.get("amount")
    destination = request.data.get("destination")
    try:
        amt = float(amount)
    except:
        return Response({"error": "invalid amount"}, status=400)
    profile = Profile.objects.get(user=request.user)
    if profile.balance < amt:
        return Response({"error": "insufficient balance"}, status=400)
    # create withdrawal request and deduct immediately (demo)
    profile.balance -= amt
    profile.save()
    w = Withdrawal.objects.create(user=request.user, amount=amt, destination=destination)
    return Response(WithdrawalSerializer(w).data)

# Admin endpoints
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_users(request):
    users = User.objects.all()
    out = []
    for u in users:
        p = Profile.objects.get(user=u)
        out.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "balance": str(p.balance),
            "is_verified": p.is_verified,
            "referral_code": p.referral_code
        })
    return Response(out)

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_verify_user(request):
    user_id = request.data.get("userId")
    try:
        u = User.objects.get(id=user_id)
        p = Profile.objects.get(user=u)
        p.is_verified = True
        p.save()
        return Response({"ok": True})
    except User.DoesNotExist:
        return Response({"error": "user not found"}, status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_post_assignment(request):
    data = request.data
    serializer = CreateAssignmentSerializer(data=data)
    if serializer.is_valid():
        a = serializer.save(posted_by_admin=True)
        return Response(AssignmentSerializer(a).data)
    return Response(serializer.errors, status=400)

