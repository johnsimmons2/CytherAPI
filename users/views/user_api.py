from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser, AllowAny
from users.serializers import UserSerializer
from users.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action


class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request: Request, view, obj) -> bool:
        return request.user == obj or request.user.is_staff or request.user.groups.filter(name='Admin').exists()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        action_perms = {
            'account_available': [AllowAny()],
            
            # Generated
            'list': [IsAdminUser()],
            'destroy': [IsAdminUser()],
            'retrieve': [IsSelfOrAdmin()],
            'update': [IsSelfOrAdmin()],
            'partial_update': [IsSelfOrAdmin()],
        }

        return action_perms.get(self.action, [IsAuthenticated()])
    
    @action(detail=False, methods=['get'])
    def account_available(self, request: Request) -> Response:
        username = request.query_params.get('u', '').strip()
        email = request.query_params.get('e', '').strip()
        
        username_available = not User.objects.filter(username=username).exists()
        email_available = not User.objects.filter(email=email).exists()
        return Response({"available": username_available and email_available}, status=200)