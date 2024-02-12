from rest_framework import serializers
from django.utils import timezone
from .models import TipoEquipamento
from equipamento.serializers import EquipamentoSerializer
from django.contrib.auth.models import User


# Serializdor para listagem de  todos os tipos de equipamentos
class TipoEquipamentoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipamento
        fields = ['id', 'tipo', 'status']



# Serializador para detalhes dos tipos de equipamentos
class TipoEquipamentoSerializer(serializers.ModelSerializer):
    # Relacionamento com Equipamentos (somente leitura)
    equipamentos = EquipamentoSerializer(many=True, read_only=True)

    # Metodos para obter o username do usuario
    def get_usuario_cadastro(self, obj):
        user = User.objects.get(id=obj.usuario_cadastro.id)
        return {"id": user.id, "username": user.username}
    
    def get_usuario_ultima_alteracao(self, obj):
        if obj.usuario_ultima_alteracao is not None:
            user = User.objects.get(id=obj.usuario_ultima_alteracao.id)
            return {"id": user.id, "username": user.username}
        return None
    
    usuario_cadastro = serializers.SerializerMethodField('get_usuario_cadastro')
    usuario_ultima_alteracao = serializers.SerializerMethodField('get_usuario_ultima_alteracao')

    class Meta:
        model = TipoEquipamento
        fields = ['id', 'tipo', 'status', 'usuario_cadastro', 'data_ultima_alteracao', 'usuario_ultima_alteracao', 'equipamentos']
        read_only_fields = ['data_ultima_alteracao', 'usuario_ultima_alteracao']

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