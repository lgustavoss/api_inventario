from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Equipamento
from .serializers import EquipamentoSerializer, EquipamentoStatusSerializer, EquipamentoColaboradorSerializer, EquipamentoEmpresaSerializer, EquipamentoSituacaoSerializer



class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        #Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')

        if page_size:
            #se 'page_size' for especificado, use o valor fornecido
            self.paginator.page_size = int(page_size)
        
        return super().list(request, *args, **kwargs)
    

class EquipamentoStatusUpdateView(APIView):
    def patch(self, request, pk):
        equipamento = Equipamento.objects.get(pk=pk)
        serializer = EquipamentoStatusSerializer(equipamento, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EquipamentoColaboradorUpdateView(APIView):
    def patch(self, request, pk):
        equipamento = Equipamento.objects.get(pk=pk)
        serializer = EquipamentoColaboradorSerializer(equipamento, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EquipamentoEmpresaUpdateView(APIView):
    def patch(self, request, pk):
        equipamento = Equipamento.objects.get(pk=pk)
        serializer = EquipamentoEmpresaSerializer(equipamento, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EquipamentoSituacaoUpdateView(APIView):
    def patch(self, request, pk):
        equipamento = Equipamento.objects.get(pk=pk)
        serializer = EquipamentoSituacaoSerializer(equipamento, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)