from rest_framework import serializers
from .models import Equipamento, TransferenciaEmpresa, TransferenciaColaborador
from empresa.models import Empresa
from colaborador.models import Colaborador


class TransferenciaColaboradorSerializer(serializers.ModelSerializer):
    colaborador_origem = serializers.PrimaryKeyRelatedField(queryset=Colaborador.objects.all())
    colaborador_destino = serializers.PrimaryKeyRelatedField(queryset=Colaborador.objects.all())

    class Meta:
        model = TransferenciaColaborador
        fields = ('colaborador_origem', 'colaborador_destino', 'data_transferencia')


class TransferenciaEmpresaSerializer(serializers.ModelSerializer):
    empresa_origem = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())
    empresa_destino = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())

    class Meta:
        model = TransferenciaEmpresa
        fields = ('empresa_origem', 'empresa_destino', 'data_transferencia')



class EquipamentoSerializer(serializers.ModelSerializer):
    transferencias_empresa = TransferenciaEmpresaSerializer(many=True, read_only=True)

    class Meta:
        model = Equipamento
        fields = '__all__'
