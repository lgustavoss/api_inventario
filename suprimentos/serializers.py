from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Categoria

# Serializador para listagem de todas as categorias
class CategoriaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id',
            'nome',
            'descricao',
            'tipo_equipamento',
            'status',
        ]

# Serializador para detalhes da categoria
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id',
            'nome',
            'descricao',
            'tipo_equipamento',
            'status',
            'data_cadastro',
            'usuario_cadastro',
            'data_ultima_alteracao',
            'usuario_ultima_alteracao'
        ]
        read_only_fields = ['data_ultima_ateracao', 'usuario_ultima_alteracao']

    # Metodos para obter o username do usuário
    def get_usuario_cadastro(self, obj):
        user = User.objects.get(id=obj.usuario_cadastro.id)
        return {"id": user.id, "username": user.username}
    
    def get_usuario_ultima_alteracao(self, obj):
        if obj.usuario_ultima_alteracao is not None:
            user = User.objects.get(id=obj.usuario_ultima_alteracao.id)
            return {"id": user.id, "username": user.username}
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Removendo chaves existentes
        representation.pop('usuario_cadastro', None)
        representation.pop('usuario_ultima_alteracao', None)

        # Adicionando as chaves personalizadas para o usuario_cadastro
        representation['usuario_cadastro_id'] = instance.usuario_cadastro.id
        representation['usuario_cadastro_username'] = instance.usuario_cadastro.username

        # Adicionando as chaves personalizadas para o usurio_ultima_alteracao
        if instance.usuario_ultima_alteracao:
            representation['usuario_ultima_alteracao_id'] = instance.usuario_ultima_alteracao.id
            representation['usuario_ultima_alteracao_username'] = instance.usuario_ultima_alteracao.username
        else:
            representation['usuario_ultima_alteracao_id'] = None
            representation['usuario_ultima_alteracao_username'] = None

        return representation
    
    def create(self, validated_data):
        user = self.context['request'].user
        categoria = Categoria.objects.create(**validated_data)
        return categoria

    
    def update(self, instance, validated_data):
        user = self.context['request'].user

        has_changed = any(field in validated_data for field in ['nome', 'descricao', 'tipo_equipamento', 'status'])

        if has_changed:
            instance.nome = validated_data.get('nome', instance.nome)
            instance.descricao = validated_data.get('descricao', instance.descricao)
            instance.status = validated_data.get('status', instance.status)
            instance.usuario_ultima_alteracao = user
            instance.data_ultima_alteracao = timezone.now() # Define data de alteracao apenas se houver mudanças
            
            instance.save()

            # Limpa os tipos de equipamento existentes e adiciona os novos tipos de equipamento
            tipo_equipamento_ids = validated_data.get('tipo_equipamento', [])
            instance.tipo_equipamento.clear()
            instance.tipo_equipamento.add(*tipo_equipamento_ids)

        return instance