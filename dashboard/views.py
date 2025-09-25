from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile
from .serializers import ProfileSerializer

# Utility: generate JWT
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "token": str(refresh.access_token),
    }

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")
    ref = request.data.get("referral")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    profile = Profile.objects.create(user=user)

    if ref:
        try:
            ref_user = User.objects.get(username=ref)
            profile.referred_by = ref_user
            profile.save()
        except:
            pass

    tokens = get_tokens_for_user(user)
    return Response(tokens)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    email_or_username = request.data.get("email")
    password = request.data.get("password")

    # allow login with either username or email
    try:
        user = User.objects.get(email=email_or_username)
        username = user.username
    except User.DoesNotExist:
        username = email_or_username

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    tokens = get_tokens_for_user(user)
    return Response(tokens)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)
