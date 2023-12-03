from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Empresa
from .serializers import EmpresaSerializer, EmpresaStatusSerializer
from equipamento.serializers import EquipamentoSerializer
from equipamento.models import Equipamento


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manipulação de Empresas.
    """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    pagination_class = PageNumberPagination


    def list(self, request, *args, **kwargs):
        """
        Lista todas as empresas com paginação opcional.
        """
        # Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')

        if page_size:
            #se 'page size' foi especificado, use o valor fornecido
            self.paginator.page_size = int(page_size)
        
        return super().list(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Atualiza parcialmente uma empresa.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retorna os detalhes de uma empresa com os equipamentos associados.
        """
        instance = self.get_object()
        equipamentos = Equipamento.objects.filter(empresa=instance)
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['equipamentos'] = EquipamentoSerializer(equipamentos, many=True).data
        return Response(data)
    

class EmpresaStatusUpdateView(APIView):
    """
    View para atualizar o status de uma empresa.
    """
    def patch(self, request, pk):
        """
        Atualiza parcialmente o status de uma empresa especificada por PK.
        """
        empresa = Empresa.objects.get(pk=pk)
        serializer = EmpresaStatusSerializer(empresa, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)