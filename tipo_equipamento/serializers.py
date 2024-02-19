from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import TipoEquipamento
from equipamento.models import Equipamento



# Serializdor para listagem de  todos os tipos de equipamentos
class TipoEquipamentoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipamento
        fields = ['id', 'tipo', 'status']



# Serializador para detalhes dos tipos de equipamentos
class TipoEquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipamento
        fields = ['id', 'tipo', 'status', 'usuario_cadastro', 'data_ultima_alteracao', 'usuario_ultima_alteracao']
        read_only_fields = ['data_ultima_alteracao', 'usuario_ultima_alteracao']

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
        tipo_equipamento = TipoEquipamento.objects.create(usuario_cadastro=user, **validated_data)
        return tipo_equipamento
    
    def update(self, instance, validated_data):
        if 'status' in validated_data and validated_data['status'] == False:
            # Verifica se o tipo de equipamento está vinculado a algum equipamento
            if instance.equipamento_set.exists():
                raise serializers.ValidationError("Não é permitido inativar um tipo de equipamento que está vinculado a um equipamento")
            
        user = self.context['request'].user

        # Verifica se houve alteração nos dados antes de atualizar
        has_changed = any(field in validated_data for field in ['tipo', 'status'])

        if has_changed:
            instance.tipo = validated_data.get('tipo', instance.tipo)
            instance.status = validated_data.get('status', instance.status)
            instance.usuario_ultima_alteracao = user
            instance.data_ultima_alteracao = timezone.now() # Defina a data de alteração apenas se houver mudanças
            instance.save()

        return instance


# Serializador para status do tipos de Equipamentos
class TipoEquipamentoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipamento
        fields = ['status']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        novo_status = validated_data.get('status')

        # Verificando se o status foi alterado
        if novo_status is not None and instance.status != novo_status:
            if novo_status is False and instance.equipamento_set.exists():
                raise serializers.ValidationError("Não é permitido inativar um tipo de equipamento que está vinculado a um equipamento")
            instance.status = novo_status
            instance.usuario_alteracao = user
            instance.data_ultima_alteracao = timezone.now() # Define a data de alteração apenas se houver mudancas
            instance.save
        elif instance.status == novo_status:
            raise serializers.ValidationError("O tipo de equipamento já possui esse status")
        
        return instance
    

# Serializador para listar os equipamentos vinculados a um tipo de equipamento
class EquipamentoTipoEquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['id', 'tag_patrimonio', 'empresa', 'colaborador', 'marca', 'modelo', 'situacao']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Removendo as chaves existentes
        representation.pop('empresa', None)
        representation.pop('colaborador', None)

        # Adicionando as chaves personalizadas
        representation['empresa_id'] = instance.empresa.id
        representation['empresa_nome'] = instance.empresa.nome
        representation['colaborador_id'] = instance.colaborador.id
        representation['colaborador_nome'] = instance.colaborador.nome
        
        return representation