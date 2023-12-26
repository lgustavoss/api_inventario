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
        
class UserSerializer(serializers.ModelSerializer):
    grupos = GrupoSerializer(many=True, read_only=True, source='groups')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'date_joined', 'last_login', 'grupos']


class UserDetailSerializer(serializers.ModelSerializer):
    grupos = GrupoDetailSerializer(many=True, read_only=True, source='groups')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'date_joined', 'last_login', 'grupos']