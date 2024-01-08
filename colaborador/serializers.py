from rest_framework import serializers
from django.utils import timezone
from .models import Colaborador
from equipamento.serializers import EquipamentoSerializer
from equipamento.models import Equipamento


# Serializador para detalhes do Colaborador
class ColaboradorSerializer(serializers.ModelSerializer):
    equipamentos = EquipamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Colaborador
        fields = ['id', 'nome', 'cpf', 'status', 'data_cadastro', 'usuario_cadastro', 'data_ultima_ateracao', 'usuario_ultima_alteracao', 'equipamentos']
        read_only_fields = ['data_ultima_ateracao', 'usuario_ultima_alteracao']

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
            instance.data_ultima_ateracao = timezone.now()  # Define a data de alteração apenas se houver mudanças
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
            instance.data_ultima_ateracao = timezone.now()  # Define a data de alteração apenas se houver mudanças
            instance.save()
        elif instance.status == novo_status:
            raise serializers.ValidationError("O colaborador já possui esse status.")

        return instance