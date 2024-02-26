from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Equipamento, TransferenciaEmpresa, TransferenciaColaborador, AlteracaiSituacaoEquipamento
from empresa.models import Empresa
from colaborador.models import Colaborador
from setor.models import Setor
from .models import Equipamento


# Serializador para Transferência de Colaborador
class TransferenciaColaboradorSerializer(serializers.ModelSerializer):
    colaborador_origem = serializers.PrimaryKeyRelatedField(queryset=Colaborador.objects.all())
    usuario_transferencia_colaborador = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = TransferenciaColaborador
        fields = [
            'id', 
            'colaborador_origem', 
            'colaborador_destino', 
            'usuario_transferencia_colaborador', 
            'data_transferencia', 
        ]

    # Métodos para obter o username do usuário
    def get_usuario_ultima_alteracao(self, obj):
        if obj.usuario_ultima_alteracao is not None:
            user = User.objects.get(id=obj.usuario_ultima_alteracao.id)
            return {"id": user.id, "username": user.username}
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Removendo chaves existentes
        representation.pop('colaborador_origem')
        representation.pop('colaborador_destino')
        representation.pop('usuario_transferencia_colaborador')
        
        # Adicionando chaves personalizadas
        representation['colaborador_origem_id'] = instance.colaborador_origem.id
        representation['colaborador_origem_nome'] = instance.colaborador_origem.nome
        representation['colaborador_destino_id'] = instance.colaborador_destino.id
        representation['colaborador_destino_nome'] = instance.colaborador_destino.nome

        # Adicionando chaves personalizadas do usuário
        representation['usuario_transferencia_colaborador_id'] = instance.usuario_transferencia_colaborador.id
        representation['usuario_transferencia_colaborador_username'] = instance.usuario_transferencia_colaborador.username

        return representation
    
    def create(self, validated_data):
        # Obtendo o colaborador atual do equipamento
        equipamento = Equipamento.objects.get(pk=validated_data['equipamento'].id)
        colaborador_origem = equipamento.colaborador

        # Obtendo o usuário logado a partir do contexto da solicitação
        usuario_transferencia_colaborador = self.context['request'].user

        # Atribuindo o colaborador de origem e o usuário logado aos campos
        validated_data['colaborador_origem'] = colaborador_origem
        validated_data['usuario_transferencia_colaborador'] = usuario_transferencia_colaborador

        # Criando a nova transferência da empresa
        transferencia = TransferenciaColaborador.objects.create(**validated_data)

        return transferencia

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
        representation['usuario_transferencia_empresa_id'] = instance.usuario_transferencia_empresa.id
        representation['usuario_transferencia_empresa_username'] = instance.usuario_transferencia_empresa.username


        return representation

    def create(self, validated_data):
        # Obtendo a empresa atual do equipamento
        equipamento = Equipamento.objects.get(pk=validated_data['equipamento'].id)
        empresa_origem = equipamento.empresa

        # Obtendo o usuario logado
        usuario_transferencia_empresa = self.context['request'].user

        # Atribuindo a empresa atual e o usuario logado aos campos
        validated_data['empresa_origem'] = empresa_origem
        validated_data['usuario_transferencia_empresa'] = usuario_transferencia_empresa

        # Criando a nova transferencia da empresa
        transferencia = TransferenciaEmpresa.objects.create(**validated_data)

        return transferencia

# Serializador para Alteracao de Situação do Equipamento
class HistoricoSituacaoEquipamentoSerializer(serializers.ModelSerializer):
    usuario_situacao_equipamento = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = AlteracaiSituacaoEquipamento
        fields = [
            'id', 
            'usuario_situacao_equipamento', 
            'situacao_anterior', 
            'situacao_nova', 
            'data_alteracao',
        ]
    
    # Metodos para obter o username do usuario
    def get_usuario_situacao_equipamento(self, obj):
        if obj.usuario_situacao_equipamento is not None:
            user = User.objects.get(id=obj.usuario_situacao_equipamento.id)
            return {"id": user.id, "username": user.username}
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Removendo chaves existentes
        representation.pop('usuario_situacao_equipamento')

        # Adicionando chaves personalizadas do usuário
        representation['usuario_situacao_equipamento_id'] = instance.usuario_situacao_equipamento.id
        representation['usuario_situacao_equipamento_username'] = instance.usuario_situacao_equipamento.username

        return representation
    
    def create(self, validated_data):
        # Obtendo a situacao atual do equipamento
        equipamento = Equipamento.objects.get(pk=validated_data['equipamento'].id)
        situacao_anterior = equipamento.situacao

        # Obtendo o usuario logado
        usuario_situacao_equipamento = self.context['request'].user

        # Atribuindo a situacao atual e o usuario logado aos campos
        validated_data['situacao_anterior'] = situacao_anterior
        validated_data['usuario_situacao_equipamento'] = usuario_situacao_equipamento

        # Criando a alteração de status
        alteracao = AlteracaiSituacaoEquipamento.objects.create(**validated_data)

        return alteracao

# Serializador para listagem de todos os equipamentos
class EquipamentoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['id', 'tag_patrimonio', 'tipo_equipamento', 'situacao', 'marca', 'modelo', 'empresa', 'colaborador', 'setor', 'status']


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Removendo chaves existentes
        representation.pop('tipo_equipamento', None)
        representation.pop('empresa', None)
        representation.pop('colaborador', None)
        representation.pop('setor', None)

        # Adicionando as chaves personalizadas
        representation['tipo_equipamento_id'] = instance.tipo_equipamento.id
        representation['tipo_equipamento_tipo'] = instance.tipo_equipamento.tipo
        representation['empresa_id'] = instance.empresa.id
        representation['empresa_nome'] = instance.empresa.nome

        # Adicionando as chaves personalizadas para colaborador
        if instance.colaborador:
            representation['colaborador_id'] = instance.colaborador.id
            representation['colaborador_nome'] = instance.colaborador.nome

        else:
            representation['colaborador_id'] = None
            representation['colaborador_nome'] = None

        # Adicionando as chaves personalizadas para setor
        if instance.setor:
            representation['setor_id'] = instance.setor.id
            representation['setor_nome'] = instance.setor.nome
        else:
            representation['setor_id'] = None
            representation['setor_nome'] = None

        return representation

# Serializador principal para Equipamento
class EquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['id', 'tag_patrimonio', 'tipo_equipamento', 'pedido', 'data_compra', 'situacao',
                  'empresa', 'colaborador', 'setor', 'marca', 'modelo', 'especificacoes', 
                  'acesso_remoto', 'acesso_id', 'acesso_senha', 'observacao', 'data_cadastro',
                  'usuario_cadastro', 'data_ultima_alteracao', 'usuario_ultima_alteracao', 'status']
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
        representation.pop('setor', None)

        # Adicionando chaves personalizdas para tipo de equipamento, empresa e colaborador
        representation['tipo_equipamento_id'] = instance.tipo_equipamento.id
        representation['tipo_equipamento_tipo'] = instance.tipo_equipamento.tipo
        representation['empresa_id'] = instance.empresa.id
        representation['empresa_nome'] = instance.empresa.nome
        
        # Adicionando as chaves personalizadas para colaborador
        if instance.colaborador:
            representation['colaborador_id'] = instance.colaborador.id
            representation['colaborador_nome'] = instance.colaborador.nome

        else:
            representation['colaborador_id'] = None
            representation['colaborador_nome'] = None

        # Adicionando as chaves personalizadas para setor
        if instance.setor:
            representation['setor_id'] = instance.setor.id
            representation['setor_nome'] = instance.setor.nome
        else:
            representation['setor_id'] = None
            representation['setor_nome'] = None

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
        setor = validated_data.pop('setor', None)
        equipamento = Equipamento.objects.create(
            usuario_cadastro=user,
            setor=setor,
            **validated_data
        )
        return equipamento

    def update(self, instance, validated_data):
        user = self.context.get('request').user

        # Atualizando campos editaveis
        campos_nao_editaveis = ['tag_patrimonio', 'empresa', 'colaborador', 'situacao']
        for campo, valor in validated_data.items():
            if campo not in campos_nao_editaveis:
                setattr(instance, campo, valor)
        
        # Atualizando data e usuario da ultima alteracao
        instance.data_ultima_alteracao = timezone.now()
        instance.usuario_ultima_alteracao = user

        # Salvando a instancia
        instance.save(update_fields=[
            'data_ultima_alteracao', 
            'usuario_ultima_alteracao', 
            'setor', 
            'pedido', 
            'marca', 
            'modelo',
            'especificacoes',
            'acesso_remoto',
            "acesso_id",
            'acesso_senha',
            'observacao',
        ])
        return instance
