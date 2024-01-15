from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

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
    

User = get_user_model()

class UpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        user = self.instance # Obtém a instância do usuário sendo atualizado
        request_user = self.context['request'].user # Obtém o usuário que está fazendo a solicitação

        # Verificando se o usuário que está fazendo a edição é admin ou o proprio usuário
        if not request_user.is_admin and request_user != user:
            raise serializers.ValidationError("Usuário sem permissão para editar esse usuário")
        return attrs
    
    def update(self, instance, validated_data):
        # Verificar se uma nova senha foi fornecida
        new_password = validated_data.get('password')

        if new_password:
            instance.password = make_password(new_password)

        # Atualizar os outros campos do usuário
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        # Salvar as alterações
        instance.save()

        return instance


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        email = value
        user = User.objects.filter(email=email).first()

        if user:
            # Criando o token para a redefinição de senha
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Construindo a URL de redefinição de senha
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

            # Enviando o e-mail de redefinição de senha
            subject = 'Redefinição de Senha'
            message = f'Clique no seguinte link para redefinir sua senha:\n\n{reset_url}'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]

            send_mail(subject, message, from_email, to_email, fail_silently=False)

        # Independentemente de encontrar ou não um usuário, retorne o valor validado
        return value

    def save(self, **kwargs):
        # Este método é chamado implicitamente, mas podemos deixá-lo vazio, pois a lógica já está na validação de e-mail
        pass