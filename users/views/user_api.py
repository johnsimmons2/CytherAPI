from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, IsAdminUser
from rest_framework.response import Response
from users.serializers import UserSerializer
from users.models import User
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth import authenticate


class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request: Request, view, obj) -> bool:
        return request.user == obj or request.user.is_staff or request.user.groups.filter(name='Admin').exists()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [IsSelfOrAdmin()]
        return [IsAuthenticated()]