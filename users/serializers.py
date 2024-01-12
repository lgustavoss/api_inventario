from django.contrib.auth.models import User, Group
from rest_framework import serializers


class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class GrupoDetailSerializer(serializers.ModelSerializer):
    permissions_list = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions_list']

    def get_permissions_list(self, obj):
        permissions = obj.permissions.values_list('name', flat=True)
        permissions_dict = {permission: obj.permissions.filter(name=permission).exists() for permission in permissions}
        return permissions_dict
    
class CreateUserSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_admin']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        is_admin = validated_data.pop('is_admin', False)
        user = User.objects.create_user(**validated_data)
        
        if is_admin:
            user.is_staff = True
            user.is_superuser = True
            user.save()
        
        return user
        
class UserSerializer(serializers.ModelSerializer):
    grupos = GrupoSerializer(many=True, read_only=True, source='groups')
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'date_joined', 'last_login', 'is_admin', 'grupos']

    def get_is_admin(self, obj):
        return obj.is_staff


class UserDetailSerializer(serializers.ModelSerializer):
    grupos = GrupoDetailSerializer(many=True, read_only=True, source='groups')
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'date_joined', 'last_login', 'is_admin', 'grupos']

    def get_is_admin(self, obj):
        return obj.is_staff