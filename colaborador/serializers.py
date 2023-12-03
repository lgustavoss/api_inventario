from rest_framework import serializers
from .models import Colaborador
from equipamento.serializers import EquipamentoSerializer


# Serializador para detalhes do Colaborador
class ColaboradorSerializer(serializers.ModelSerializer):
    # Relacionamento com Equipamentos (somente leitura)
    equipamentos = EquipamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Colaborador
        fields = ['id', 'nome', 'cpf', 'status', 'equipamentos']

# Serializador para status do Colaborador
class ColaboradorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = ['status']
