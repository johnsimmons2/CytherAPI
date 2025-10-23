import os
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from users.models.user import User
from cytherapi.utils import OK, BAD_REQUEST, UNAUTHORIZED
from django.core.mail import send_mail
from users.serializers import UserSerializer

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request: Request) -> JsonResponse:
    data = request.data
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate(request, username=username, password=password)
    user_data = UserSerializer(user).data
    if user is not None:
        login(request, user)
        return OK("Login successful.", user=user_data)
    else:
        return UNAUTHORIZED("Invalid username or password.")

@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request: Request) -> JsonResponse:
    if not request.user.is_authenticated:
        return BAD_REQUEST("You are not logged in.")

    logout(request)
    return OK("Logout successful.")

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request: Request) -> JsonResponse:
    data = request.data
    # Required
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    
    # Optional
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    
    if not username or not password:
        return BAD_REQUEST("Username and password are required.")

    if User.objects.filter(username=username).exists():
        return BAD_REQUEST("Username already exists.")
    
    if User.objects.filter(email=email).exists():
        return BAD_REQUEST("Email already exists.")
    
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        group = Group.objects.get(name="Guest")
        user.groups.add(group)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        login(request, user)
        send_mail(
            'Welcome to Cyther.online',
            f'Hello {user.username},\n\nThank you for registering on Cyther. We hope you enjoy your experience.\n\nBest regards,\nCyther Team',
            os.getenv('EMAIL_FROM_DISPLAY', 'admin@cyther.online'),
            [user.email]
        )
        return OK("User registered successfully.", username=user.username)
    except IntegrityError:
        return BAD_REQUEST("Username already exists.")
    

@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def auth_check(request: Request) -> JsonResponse:
    groups = list(request.user.groups.values_list('name', flat=True))
    user_data = UserSerializer(request.user).data
    
    return OK("success", groups=groups, user=user_data)