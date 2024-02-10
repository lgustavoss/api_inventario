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
        fields = ('colaborador_origem', 'colaborador_destino', 'data_transferencia', 'usuario_transferencia_colaborador')
        extra_kwargs = {
            'usuario_transferencia_colaborador': {'required': False}
        }


# Serializador para Transferência de Empresa
class TransferenciaEmpresaSerializer(serializers.ModelSerializer):
    empresa_origem = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())
    empresa_destino = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())

    class Meta:
        model = TransferenciaEmpresa
        fields = ('empresa_origem', 'empresa_destino', 'data_transferencia', 'usuario_transferencia_empresa')
        extra_kwargs = {
            'usuario_transferencia_empresa': {'required': False}
        }


class HistoricoSituacaoEquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlteracaiSituacaoEquipamento
        fields = ('situacao_anterior', 'situacao_nova', 'data_alteracao', 'equipamento', 'usuario_situacao_equipamento')


# Serializador para Alteração de Situação do Equipamento
class AlteracaoSituacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['situacao']


# Serializador principal para Equipamento
class EquipamentoSerializer(serializers.ModelSerializer):

    empresa_nome = serializers.CharField(source='empresa.nome', read_only=True)
    empresa_id = serializers.IntegerField(source='empresa.id', write_only=True)
    colaborador_nome = serializers.CharField(source='colaborador.nome', read_only=True)
    colaborador_id = serializers.IntegerField(write_only=True)
    tipo_equipamento_nome = serializers.CharField(source='tipo_equipamento.tipo', read_only=True)
    tipo_equipamento_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Equipamento
        fields = ['id', 'tag_patrimonio', 'tipo_equipamento_nome', 'tipo_equipamento_id', 'pedido', 'data_compra', 'situacao',
                  'empresa_nome', 'empresa_id', 'colaborador_nome', 'colaborador_id', 'marca', 'modelo', 'especificacoes', 'acesso_remoto',
                  'acesso_id', 'acesso_senha', 'observacao', 'data_cadastro', 'usuario_cadastro',
                  'data_ultima_alteracao', 'usuario_ultima_alteracao', 'status']
        read_only_fields = ['data_ultima_alteracao', 'usuario_ultima_alteracao']

    def create(self, validated_data):
        user = self.context.get('request').user
        tipo_equipamento_id = validated_data.pop('tipo_equipamento_id', None)
        tipo_equipamento = None
        empresa_id = validated_data.pop('empresa_id', None)
        empresa = None
        colaborador_id = validated_data.pop('colaborador_id', None)
        colaborador = None

        if colaborador_id:
            # Usar o ID fornecido para obter o Colaborador
            colaborador = Colaborador.objects.get(pk=colaborador_id)

        if empresa_id:
            # Usar o ID fornecido para obter a Empresa
            empresa = Empresa.objects.get(pk=empresa_id)

        if tipo_equipamento_id:
            # Usar o ID fornecido para obter o TipoEquipamento
            tipo_equipamento = TipoEquipamento.objects.get(pk=tipo_equipamento_id)
        
        equipamento = Equipamento.objects.create(
            usuario_cadastro=user,
            tipo_equipamento=tipo_equipamento,
            empresa=empresa,
            colaborador=colaborador,
            **validated_data
        )
        return equipamento

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['empresa_id'] = instance.empresa.id if instance.empresa else None
        return representation

    def update(self, instance, validated_data):
        campos_nao_editaveis = ['tag_patrimonio', 'empresa', 'colaborador', 'situacao']

        for campo, valor in validated_data.items():
            if campo not in campos_nao_editaveis:
                setattr(instance, campo, valor)
        
        instance.save()
        return instance