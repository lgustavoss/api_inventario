from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Empresa
from equipamento.models import Equipamento
from equipamento.serializers import EquipamentoSerializer



# Serializador para listagem de todas as empresas
class EmpresaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nome', 'cnpj', 'status']

# Serializador para detalhes da Empresa
class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nome', 'cnpj', 'status', 'data_cadastro', 'usuario_cadastro', 'data_ultima_alteracao', 'usuario_ultima_alteracao']
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
    

# Serializer para listar os equipamentos vinculados a uma empresa
class EquipamentoEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['id', 'tag_patrimonio','tipo_equipamento', 'colaborador', 'marca', 'modelo', 'situacao']

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