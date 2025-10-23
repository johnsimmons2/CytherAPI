from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'groups', 'last_login', 'date_joined', 'is_staff', 'is_active']
        read_only_fields = ['id', 'email', 'username', 'last_login', 'date_joined']
        