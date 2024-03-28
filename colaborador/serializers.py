from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Colaborador
from equipamento.models import Equipamento



# Serializador para listagem de todos os colaboradores
class ColaboradorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = ['id', 'nome', 'cpf', 'status']

# Serializador para detalhes do Colaborador
class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = ['id', 'nome', 'cpf', 'status', 'data_cadastro', 'usuario_cadastro', 'data_ultima_alteracao', 'usuario_ultima_alteracao']
        read_only_fields = ['data_ultima_ateracao', 'usuario_ultima_alteracao']

    # Metodos para obter o username do usuario
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

        # Removendo as chaves existentes
        representation.pop('usuario_cadastro', None)
        representation.pop('usuario_ultima_alteracao', None)

        # Adicionando as chaves personalizadas para usuario_cadastro
        representation['usuario_cadastro_id'] = instance.usuario_cadastro.id
        representation['usuario_cadastro_username'] = instance.usuario_cadastro.username

        # Adicionando as chaves personalizadas para usuario_ultima_alteracao
        if instance.usuario_ultima_alteracao:
            representation['usuario_ultima_alteracao_id'] = instance.usuario_ultima_alteracao.id
            representation['usuario_ultima_alteracao_username'] = instance.usuario_ultima_alteracao.username
        else:
            representation['usuario_ultima_alteracao_id'] = None
            representation['usuario_ultima_alteracao_username'] = None

        return representation

    def create(self, validated_data):
        user = self.context['request'].user
        colaborador = Colaborador.objects.create(usuario_cadastro=user, **validated_data)
        return colaborador

    def update(self, instance, validated_data):
        if 'status' in validated_data and validated_data['status'] == False:
            # Verifica se o colaborador está vinculado a algum equipamento
            if instance.equipamento_set.exists():
                raise serializers.ValidationError("Não é permitido inativar um colaborador que está vinculado a um equipamento.")

        user = self.context['request'].user

        # Verifica se houve alteração nos dados antes de atualizar
        has_changed = any(field in validated_data for field in ['nome', 'cpf', 'status'])
        
        if has_changed:
            instance.nome = validated_data.get('nome', instance.nome)
            instance.cpf = validated_data.get('cpf', instance.cpf)
            instance.status = validated_data.get('status', instance.status)
            instance.usuario_ultima_alteracao = user
            instance.data_ultima_alteracao = timezone.now()  # Define a data de alteração apenas se houver mudanças
            instance.save()

        return instance

# Serializador para status do Colaborador
class ColaboradorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = ['status']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        novo_status = validated_data.get('status')

        # Verifica se o status foi alterado
        if novo_status is not None and instance.status != novo_status:
            if novo_status is False and instance.equipamento_set.exists():
                raise serializers.ValidationError("Não é permitido inativar um colaborador que está vinculado a um equipamento.")
                
            instance.status = novo_status
            instance.usuario_ultima_alteracao = user
            instance.data_ultima_alteracao = timezone.now()  # Define a data de alteração apenas se houver mudanças
            instance.save()
        elif instance.status == novo_status:
            raise serializers.ValidationError("O colaborador já possui esse status.")

        return instance

# Serializer para listar os equipamentos vinculados a um colaborador
class EquipamentoColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['id', 'tag_patrimonio', 'tipo_equipamento', 'empresa', 'marca', 'modelo', 'situacao']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Removendo as chaves existentes
        representation.pop('tipo_equipamento', None)
        representation.pop('empresa', None)

        # Adicionando as chaves personalizadas
        representation['tipo_equipamento_id'] = instance.tipo_equipamento.id
        representation['tipo_equipamento_tipo'] = instance.tipo_equipamento.tipo
        representation['empresa_id'] = instance.empresa.id
        representation['empresa_nome'] = instance.empresa.nome
        
        return representation