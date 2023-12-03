from rest_framework import serializers
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
    empresa_nome = serializers.SerializerMethodField()
    colaborador_nome = serializers.SerializerMethodField()
    tipo_equipamento_nome = serializers.SerializerMethodField()
    
    class Meta:
        model = Equipamento
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def update(self, instance, validated_data):
        campos_nao_editaveis = ['tag_patrimonio', 'empesa', 'colaborador', 'situacao']

        for campo, valor in validated_data.items():
            if campo not in campos_nao_editaveis:
                setattr(instance, campo, valor)
        
        instance.save()
        return instance
    
    def get_empresa_nome(self, obj):
        return obj.empresa.nome if obj.empresa else None

    def get_colaborador_nome(self, obj):
        return obj.colaborador.nome if obj.colaborador else None

    def get_tipo_equipamento_nome(self, obj):
        return obj.tipo_equipamento.tipo if obj.tipo_equipamento else None