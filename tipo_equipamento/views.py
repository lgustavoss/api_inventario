from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .serializers import TipoEquipamentoSerializer
from .models import TipoEquipamento


class TipoEquipamentoViewSet(viewsets.ModelViewSet):
    queryset = TipoEquipamento.objects.all()
    serializer_class = TipoEquipamentoSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        #Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')

        if page_size:
            #se 'page_size' for especificado, use o valor fornecido
            self.paginator.page_size = int(page_size)

        return super().list(request, *args, **kwargs)