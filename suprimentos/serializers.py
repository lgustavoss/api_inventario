from rest_framework import serializers
from .models import Categoria
from .utils import get_ancestors, get_descendentes
from tipo_equipamento.models import TipoEquipamento

class CategoriaPaiSerialier(serializers.ModelSerializer):
    tipo_equipamentos = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TipoEquipamento.objects.all()
    )
    ancestors = serializers.SerializerMethodField()
    descendentes = serializers.SerializerMethodField()

    def get_ancestors(self, obj):
        return get_ancestors(obj)
    
    def get_descendentes(self, obj):
        return get_descendentes(obj)
    
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'pai', 'tipo_equipamentos', 'ancestors', 'descendentes']

class CategoriaFilhaSerializer(serializers.ModelSerializer):
    ancestors = serializers.SerializerMethodField()
    descendentes = serializers.SerializerMethodField()

    tipo_equipamentos = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TipoEquipamento.objects.all(), required=False
    )
    
    def get_ancestors(self, obj):
        return get_ancestors(obj)

    def get_descendentes(self, obj):
        return get_descendentes(obj)

    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'pai', 'ancestors', 'descendentes']
