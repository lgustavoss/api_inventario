from rest_framework import serializers
from .models import Equipamento, TransferenciaEmpresa, TransferenciaColaborador, AlteracaiSituacaoEquipamento
from empresa.models import Empresa
from colaborador.models import Colaborador
from tipo_equipamento.models import TipoEquipamento
from django.contrib.auth.models import User


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


# Serializador para listagem de todos os equipamentos
class EquipamentoListSerializer(serializers.ModelSerializer):
    # Metodo para obter id e nome do tipo de equipamento
    def get_tipo_equipamento(self, obj):
        tipo_equipamento = TipoEquipamento.objects.get(id=obj.tipo_equipamento.id)
        return {"id": tipo_equipamento.id, "tipo": tipo_equipamento.tipo}
    
    # Metodo para obter id e nome da empresa
    def get_empresa(self, obj):
        empresa = Empresa.objects.get(id=obj.empresa.id)
        return {"id": empresa.id, "nome": empresa.nome}
    
    # Metodo para obter id e nome do colaborador
    def get_colaborador(selg, obj):
        colaborador = Colaborador.objects.get(id=obj.colaborador.id)
        return {"id": colaborador.id, "nome": colaborador.nome}

    tipo_equipamento = serializers.SerializerMethodField('get_tipo_equipamento')
    empresa = serializers.SerializerMethodField('get_empresa')
    colaborador = serializers.SerializerMethodField('get_colaborador')

    class Meta:
        model = Equipamento
        fields = ['id', 'tag_patrimonio', 'tipo_equipamento', 'situacao', 'marca', 'modelo', 'empresa', 'colaborador', 'status']


# Serializador principal para Equipamento
class EquipamentoSerializer(serializers.ModelSerializer):

    # Metodo para obter id e nome do tipo de equipamento
    def get_tipo_equipamento(self, obj):
        tipo_equipamento = TipoEquipamento.objects.get(id=obj.tipo_equipamento.id)
        return {"id": tipo_equipamento.id, "tipo": tipo_equipamento.tipo}
    
    # Metodo para obter id e nome da empresa
    def get_empresa(self, obj):
        empresa = Empresa.objects.get(id=obj.empresa.id)
        return {"id": empresa.id, "nome": empresa.nome}
    
    # Metodo para obter id e nome do colaborador
    def get_colaborador(selg, obj):
        colaborador = Colaborador.objects.get(id=obj.colaborador.id)
        return {"id": colaborador.id, "nome": colaborador.nome}
    
    # Metodos para obter o username do usuario
    def get_usuario_cadastro(self, obj):
        user = User.objects.get(id=obj.usuario_cadastro.id)
        return {"id":user.id, "username": user.username}
    
    def get_usuario_ultima_alteracao(self, obj):
        if obj.usuario_ultima_alteracao is not None:
            user = User.objects.get(id=obj.usuario_ultima_alteracao.id)
            return {"id": user.id, "username": user.username}
        return None

    tipo_equipamento = serializers.SerializerMethodField('get_tipo_equipamento')
    empresa = serializers.SerializerMethodField('get_empresa')
    colaborador = serializers.SerializerMethodField('get_colaborador')
    usuario_cadastro = serializers.SerializerMethodField('get_usuario_cadastro')
    usuario_ultima_alteracao = serializers.SerializerMethodField('get_usuario_ultima_alteracao')

    class Meta:
        model = Equipamento
        fields = ['id', 'tag_patrimonio', 'tipo_equipamento', 'pedido', 'data_compra', 'situacao',
                  'empresa', 'colaborador', 'marca', 'modelo', 'especificacoes', 'acesso_remoto',
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