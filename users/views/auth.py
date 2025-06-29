import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.http import JsonResponse
from django.http.request import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from users.models.user import User
from cytherapi.utils import OK, BAD_REQUEST, UNAUTHORIZED


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: Request) -> JsonResponse:
    data = request.data
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return OK("Login successful.", username=user.username)
    else:
        return UNAUTHORIZED("Invalid username or password.")

@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request: Request) -> JsonResponse:
    if not request.user.is_authenticated:
        return BAD_REQUEST("You are not logged in.")

    logout(request)
    return OK("Logout successful.")
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request: Request) -> JsonResponse:
    data = request.data
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
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
    except IntegrityError:
        return BAD_REQUEST("Username already exists.")
    
    return OK("User registered successfully.", username=user.username)