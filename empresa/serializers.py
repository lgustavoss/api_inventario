from rest_framework import serializers
from .models import Empresa
from equipamento.serializers import EquipamentoSerializer


# Serializador para detalhes da Empresa
class EmpresaSerializer(serializers.ModelSerializer):
    # Relacionamento com Equipamentos (somente leitura)
    equipamentos = EquipamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Empresa
        fields = ['id', 'nome', 'cnpj', 'status', 'equipamentos']

# Serializador para status da Empresa
class EmpresaStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['status']