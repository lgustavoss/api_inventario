from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Colaborador
from .serializers import ColaboradorSerializer, ColaboradorStatusSerializer


class ColaboradorViewSet(viewsets.ModelViewSet):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        #Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')

        if page_size:
            #se 'page_size' for especificado, use o valor fornecido
            self.paginator.page_size = int(page_size)
        
        return super().list(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class ColaboradorStatusUpdateView(APIView):
    def patch(self, request, pk):
        colaborador = Colaborador.objects.get(pk=pk)
        serializer = ColaboradorStatusSerializer(colaborador, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)