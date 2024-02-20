from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Setor


# Serializador para listagem de todos os setores
class SetorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = ['id', 'nome', 'status']

# Serializador para detalhes de um setor
class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = ['id', 'nome', 'status', 'data_cadastro', 'usuario_cadastro', 'data_ultima_alteracao', 'usuario_ultima_alteracao']
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
        setor = Setor.objects.create(usuario_cadastro=user, **validated_data)
        return setor
    
    def update(self, instance, validated_data):
        if 'status' in validated_data and validated_data['status'] == False:
            # Verificando se o setor está vinculado a alguma empresa
            if instance.empresa_set.exists():
                raise serializers.ValidationError("Não é permitido inativar um setor vinculado a uma empresa")
            
        user = self.context['request'].user

        # Verifica se houve alteracao nos dados antes de atualizar
        has_changed = any(field in validated_data for field in ['nome', 'status'])

        if has_changed:
            instance.nome = validated_data.get('nome', instance.nome)
            instance.status = validated_data.get('status', instance.status)
            instance.usuario_ultima_alteracao = user
            instance.data_ultima_alteracao = timezone.now() #Define a data de alteração apenas se houver mudanças
            instance.save
        
        return instance
    
# Serializador para status do setor
class SetorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = ['status']
    
        def update(self, instance, validated_data):
            user = self.context['request'].user
            novo_status = validated_data.get('status')

            #Verifica se o status foi alterado
            if novo_status is not None and instance.status != novo_status:
                if novo_status is False and instance.equipamento_set.exists():
                    raise serializers.ValidationError("Não é permitido inativar um setor que está vinculada a uma empresa")
                instance.status = novo_status
                instance.usuario_ultima_alteracao = user
                instance.data_ultima_alteracao = timezone.now() # Define a data de alteração apenas se houver mudanças
                instance.save()
            elif instance.status == novo_status:
                raise serializers.ValidationError("O setor já possui esse status.")
            
            return instance

