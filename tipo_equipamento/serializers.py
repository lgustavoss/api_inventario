from rest_framework import serializers
from .models import TipoEquipamento


class TipoEquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipamento
        fields = '__all__'