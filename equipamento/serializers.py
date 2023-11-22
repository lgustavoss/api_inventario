from rest_framework import serializers
from .models import Equipamento


class EquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = '__all__'


class EquipamentoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['status']


class EquipamentoColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['colaborador']


class EquipamentoEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['empresa']


class EquipamentoSituacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = ['situacao']