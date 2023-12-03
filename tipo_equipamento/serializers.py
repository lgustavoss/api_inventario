from rest_framework import serializers
from .models import TipoEquipamento
from equipamento.serializers import EquipamentoSerializer


# Serializador para detalhes dos tipos de equipamentos
class TipoEquipamentoSerializer(serializers.ModelSerializer):
    # Relacionamento com Equipamentos (somente leitura)
    equipamentos = EquipamentoSerializer(many=True, read_only=True)

    class Meta:
        model = TipoEquipamento
        fields = ['id', 'tipo', 'status', 'equipamentos']

# Serializador para status do tipos de Equipamentos
class TipoEquipamentoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipamento
        fields = ['status']