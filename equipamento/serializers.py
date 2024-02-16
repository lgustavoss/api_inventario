from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Equipamento, TransferenciaEmpresa, TransferenciaColaborador, AlteracaiSituacaoEquipamento
from empresa.models import Empresa
from colaborador.models import Colaborador
from tipo_equipamento.models import TipoEquipamento
from .models import Equipamento


# Serializador para Transferência de Colaborador
class TransferenciaColaboradorSerializer(serializers.ModelSerializer):
    colaborador_origem_id = serializers.IntegerField(source='colaborador_origem.id')
    colaborador_origem_nome = serializers.CharField(source='colaborador_origem.nome')
    colaborador_destino_id = serializers.IntegerField(source='colaborador_destino.id')
    colaborador_destino_nome = serializers.CharField(source='colaborador_destino.nome')
    usuario_transferencia_colaborador_id = serializers.IntegerField(source='usuario_transferencia_colaborador.id')
    usuario_transferencia_colaborador_nome = serializers.CharField(source='usuario_transferencia_colaborador.username')

    class Meta:
        model = TransferenciaColaborador
        fields = fields = [
            'id', 
            'colaborador_origem_id', 
            'colaborador_origem_nome', 
            'colaborador_destino_id', 
            'colaborador_destino_nome', 
            'usuario_transferencia_colaborador_id', 
            'usuario_transferencia_colaborador_nome', 
            'data_transferencia', 
        ]

# Serializador para Transferência de Empresa
class TransferenciaEmpresaSerializer(serializers.ModelSerializer):
    empresa_origem = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())
    usuario_transferencia_empresa = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = TransferenciaEmpresa
        fields = [
            'id',
            'empresa_origem',
            'empresa_destino',
            'usuario_transferencia_empresa',
            'data_transferencia'
        ]

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

        # Removendo chaves existentes
        representation.pop('empresa_origem')
        representation.pop('empresa_destino')
        representation.pop('usuario_transferencia_empresa')
        
        # Adicionando as chaves personalizadas
        representation['empresa_origem_id'] = instance.empresa_origem.id
        representation['empresa_origem_nome'] = instance.empresa_origem.nome
        representation['empresa_destino_id'] = instance.empresa_destino.id
        representation['empresa_destino_nome'] = instance.empresa_destino.nome

        # Adicionando chaves personalizadas do usuário
        if instance.usuario_transferencia_empresa:
            representation['usuario_transferencia_empresa_id'] = instance.usuario_transferencia_empresa.id
            representation['usuario_transferencia_empresa_username'] = instance.usuario_transferencia_empresa.username
        else:
            representation['usuario_transferencia_empresa_id'] = None
            representation['usuario_transferencia_empresa_username'] = None

        return representation

    def create(self, validated_data):
        # Obtendo a empresa atual do equipamento
        equipamento = Equipamento.objects.get(pk=validated_data['equipamento'].id)
        empresa_origem = equipamento.empresa

        # Obtendo o usuario logado
        usuario_transferencia_empresa = self.context['request'].user

        # Atribuindo a empresa atual e o usuario loado aos campos
        validated_data['empresa_origem'] = empresa_origem
        validated_data['usuario_transferencia_empresa'] = usuario_transferencia_empresa

        # Criando a nova transferencia da empresa
        transferencia = TransferenciaEmpresa.objects.create(**validated_data)

        return transferencia

# Serializador para Situação do Equipamento
class HistoricoSituacaoEquipamentoSerializer(serializers.ModelSerializer):
    usuario_situacao_equipamento_id = serializers.IntegerField(source='usuario_situacao_equipamento.id')
    usuario_situacao_equipamento_nome = serializers.CharField(source='usuario_situacao_equipamento.username')

    class Meta:
        model = AlteracaiSituacaoEquipamento
        fields = [
            'id', 
            'usuario_situacao_equipamento_id', 
            'usuario_situacao_equipamento_nome', 
            'situacao_anterior', 
            'situacao_nova', 
            'data_alteracao', 
            'equipamento']
    

    

# Serializador para Alteração de Situação do Equipamento
class AlteracaoSituacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['situacao']

# Serializador para listagem de todos os equipamentos
class EquipamentoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['id', 'tag_patrimonio', 'tipo_equipamento', 'situacao', 'marca', 'modelo', 'empresa', 'colaborador', 'status']


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Removendo chaves existentes
        representation.pop('tipo_equipamento', None)
        representation.pop('empresa', None)
        representation.pop('colaborador', None)

        # Adicionando as chaves personalizadas
        representation['tipo_equipamento_id'] = instance.tipo_equipamento.id
        representation['tipo_equipamento_tipo'] = instance.tipo_equipamento.tipo
        representation['empresa_id'] = instance.empresa.id
        representation['empresa_nome'] = instance.empresa.nome
        representation['colaborador_id'] = instance.colaborador.id
        representation['colaborador_nome'] = instance.colaborador.nome

        return representation

# Serializador principal para Equipamento
class EquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['id', 'tag_patrimonio', 'tipo_equipamento', 'pedido', 'data_compra', 'situacao',
                  'empresa', 'colaborador', 'marca', 'modelo', 'especificacoes', 'acesso_remoto',
                  'acesso_id', 'acesso_senha', 'observacao', 'data_cadastro', 'usuario_cadastro',
                  'data_ultima_alteracao', 'usuario_ultima_alteracao', 'status']
        read_only_fields = ['data_ultima_alteracao', 'usuario_ultima_alteracao']
    
    # Metodos para obter o username do usuario
    def get_usuario_cadastro(self, obj):
        user = User.objects.get(id=obj.usuario_cadastro.id)
        return {"id":user.id, "username": user.username}
    
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
        representation.pop('tipo_equipamento', None)
        representation.pop('empresa', None)
        representation.pop('colaborador', None)

        # Adicionando chaves personalizdas para tipo de equipamento, empresa e colaborador
        representation['tipo_equipamento_id'] = instance.tipo_equipamento.id
        representation['tipo_equipamento_tipo'] = instance.tipo_equipamento.tipo
        representation['empresa_id'] = instance.empresa.id
        representation['empresa_nome'] = instance.empresa.nome
        representation['colaborador_id'] = instance.colaborador.id
        representation['colaborador_nome'] = instance.colaborador.nome

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

    def update(self, instance, validated_data):
        campos_nao_editaveis = ['tag_patrimonio', 'empresa', 'colaborador', 'situacao']

        for campo, valor in validated_data.items():
            if campo not in campos_nao_editaveis:
                setattr(instance, campo, valor)
        
        instance.save()
        return instance
    
