from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', 'role']
        read_only_fields = ['id', 'email', 'username', 'last_login', 'date_joined']
        