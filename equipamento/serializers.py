from rest_framework import serializers
from django.utils import timezone
from .models import Equipamento, TransferenciaEmpresa, TransferenciaColaborador, AlteracaiSituacaoEquipamento
from empresa.models import Empresa
from colaborador.models import Colaborador
from tipo_equipamento.models import TipoEquipamento


# Serializador para Transferência de Colaborador
class TransferenciaColaboradorSerializer(serializers.ModelSerializer):
    colaborador_origem = serializers.PrimaryKeyRelatedField(queryset=Colaborador.objects.all())
    colaborador_destino = serializers.PrimaryKeyRelatedField(queryset=Colaborador.objects.all())

    class Meta:
        model = TransferenciaColaborador
        fields = ('colaborador_origem', 'colaborador_destino', 'data_transferencia')


# Serializador para Transferência de Empresa
class TransferenciaEmpresaSerializer(serializers.ModelSerializer):
    empresa_origem = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())
    empresa_destino = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())

    class Meta:
        model = TransferenciaEmpresa
        fields = ('empresa_origem', 'empresa_destino', 'data_transferencia')


class HistoricoSituacaoEquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlteracaiSituacaoEquipamento
        fields = '__all__'


# Serializador para Alteração de Situação do Equipamento
class AlteracaoSituacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['situacao']


# Serializador principal para Equipamento
class EquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['id', 'tag_patrimonio', 'tipo_equipamento', 'pedido', 'data_compra', 'situacao',
                  'empresa', 'colaborador', 'marca', 'modelo', 'especificacoes', 'acesso_remoto',
                  'acesso_id', 'acesso_senha', 'observacao', 'data_cadastro', 'usuario_cadastro',
                  'data_ultima_alteracao', 'usuario_ultima_alteracao', 'status']
        read_only_fields = ['data_ultima_alteracao', 'usuario_ultima_alteracao']

    def create(self, validated_data):
        user = self.context.get('request').user
        equipamento = Equipamento.objects.create(usuario_cadastro=user, **validated_data)
        return equipamento

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def update(self, instance, validated_data):
        user = self.context['request'].user
        campos_nao_editaveis = ['tag_patrimonio', 'empresa', 'colaborador', 'situacao']

        for campo, valor in validated_data.items():
            if campo not in campos_nao_editaveis:
                setattr(instance, campo, valor)
        
        instance.save()
        return instance