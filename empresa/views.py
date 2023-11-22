from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Empresa
from .serializers import EmpresaSerializer, EmpresaStatusSerializer


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')

        if page_size:
            #se 'page size' foi especificado, use o valor fornecido
            self.paginator.page_size = int(page_size)
        
        return super().list(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    

class EmpresaStatusUpdateView(APIView):
    def patch(self, request, pk):
        empresa = Empresa.objects.get(pk=pk)
        serializer = EmpresaStatusSerializer(empresa, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)