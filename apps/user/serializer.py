from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import DetailPermission, Permission, Profile, User

class PermissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Permission
        fields = '__all__'

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'names', 'email', 'lastname', 
                'username', 'password', 'is_active', 'profile')


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = '__all__'


class DetailPermissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DetailPermission
        fields = ('id', 'permission', 'state')


class LoginPermission(serializers.ModelSerializer):
    permission = serializers.ReadOnlyField(source='permission.description')
    ref = serializers.ReadOnlyField(source='permission.ref')
    
    class Meta:
        model = DetailPermission
        fields = ('permission', 'ref', 'state')


class UserLogin(serializers.ModelSerializer):
    # user_permission = LoginPermission(many=True)
    profile_description = serializers.ReadOnlyField(source='profile.description')
    
    class Meta:
        model = User
        fields = '__all__'


class TokenSerializer(TokenObtainPairSerializer):
    pass
