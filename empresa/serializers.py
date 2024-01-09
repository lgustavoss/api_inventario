from rest_framework import serializers
from django.utils import timezone
from .models import Empresa
from equipamento.serializers import EquipamentoSerializer


# Serializador para detalhes da Empresa
class EmpresaSerializer(serializers.ModelSerializer):
    # Relacionamento com Equipamentos (somente leitura)
    equipamentos = EquipamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Empresa
        fields = ['id', 'nome', 'cnpj', 'status', 'data_cadastro', 'usurario_cadastro', 'data_ultimo_alteracao', 'usuario_ultima_alteracao', 'equipamentos']
        read_only_fields = ['data_ultima_alteracao', 'usuario_ultima_alteracao']

    def create(self, validated_data):
        user = self.context['request'].user
        empresa = Empresa.objects.create(usuario_cadastro=user, **validated_data)
        return empresa
    
    def update(self, instance, validated_data):
        if 'status' in validated_data and validated_data['status'] == False:
            #verifica se a empresa está vinculada a algum equipamento
            if instance.equipamento_set.exists():
                raise serializers.ValidationError("Não é permitido inativar uma empresa que está vinculada a um equipamento")
        
        user = self.context['request'].user

        # Verifica se houve alteração nos dados antes de atualizar
        has_changed = any(field in validated_data for field in ['nome', 'cnpj', 'status'])

        if has_changed:
            instance.nome = validated_data.get('nome', instance.nome)
            instance.cnpj = validated_data.get('cnpj', instance.cnpj)
            instance.status = validated_data.get('status', instance.status)
            instance.usuario_ultima_alteracao = user
            instance.data_ultima_alteracao = timezone.now() #Define a data de alteração apenas se houver mudanças
            instance.save
        
        return instance

# Serializador para status da Empresa
class EmpresaStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['status']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        novo_status = validated_data.get('status')

        #Verifica se o status foi alterado
        if novo_status is not None and instance.status != novo_status:
            if novo_status is False and instance.equipamento_set.exists():
                raise serializers.ValidationError("Não é permitido inativar uma empresa que está vinculada a um equipamento")
            instance.status = novo_status
            instance.usuario_ultima_alteracao = user
            instance.data_ultima_alteracao = timezone.now() # Define a data de alteração apenas se houver mudanças
            instance.save()
        elif instance.status == novo_status:
            raise serializers.ValidationError("A empresa já possui esse status.")
        
        return instance