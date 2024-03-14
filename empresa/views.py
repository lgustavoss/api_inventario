from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from .models import Empresa
from equipamento.models import SITUACAO_EQUIPAMENTO_CHOICES
from .serializers import EmpresaSerializer, EmpresaListSerializer, EmpresaStatusSerializer, EquipamentoEmpresaSerializer
from users.views import has_permission_to_view_empresa, has_permission_to_detail_empresa, has_permission_to_edit_empresa, has_permission_to_view_equipamento



class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manipulação de Empresas.
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return EmpresaListSerializer
        return EmpresaSerializer
    
    def get_queryset(self):
        queryset = Empresa.objects.all()
        # Filtre o queryset de acordo com as permissões do usuario
        if not has_permission_to_view_empresa(self.request.user):
            return Empresa.objects.none()
        return queryset


    def list(self, request, *args, **kwargs):
        """
        Lista todas as empresas com paginação opcional.
        """
        # Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')

        if has_permission_to_view_empresa(request.user):
            if page_size:
                #se 'page size' foi especificado, use o valor fornecido
                self.paginator.page_size = int(page_size)
            
            return super().list(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar empresas'}, status=status.HTTP_403_FORBIDDEN)
        
    
    def create(self, request, *args, **kwargs):
        if has_permission_to_edit_empresa(request.user):
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Usuário sem permissão para cadastrar uma empresa'})

    def update(self, request, *args, **kwargs):
        if has_permission_to_edit_empresa(request.user):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'error': 'Usuário sem permissão para editar empresa'}, status=status.HTTP_403_FORBIDDEN)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Atualiza parcialmente uma empresa.
        """
        if has_permission_to_edit_empresa(request.user):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para editar empresas'}, status=status.HTTP_403_FORBIDDEN)
    

    def retrieve(self, request, *args, **kwargs):
        # Retorna os detalhes de uma empresa semos equipamentos associados.
        if has_permission_to_detail_empresa(request.user):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar os detalhes de uma empresa'}, status=status.HTTP_403_FORBIDDEN)
    
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

        if has_permission_to_edit_empresa(request.user):
            serializer = EmpresaStatusSerializer(empresa, data=request.data, partial=True, context={'context': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuário sem permissão para alterar status de empresa'}, status=status.HTTP_403_FORBIDDEN)
        
class EquipamentosEmpresaView(generics.ListAPIView):
    serializer_class = EquipamentoEmpresaSerializer

    def get_queryset(self):
        empresa_id = self.kwargs['pk']
        empresa = Empresa.objects.get(pk=empresa_id)

        # Verificando se o usuario tem permissao para visualizar equipamentos
        if has_permission_to_view_equipamento(self.request.user):
            queryset = empresa.equipamento_set.all()

            # Acessando o valor do page_size na consulta
            page_size = self.request.query_params.get('page_size')
            if page_size:
                self.paginator.page_size = int(page_size)
            return queryset
        else:
            return Response({'error': 'Usuário sem permissão para visualizar equipamentos'}, status=status.HTTP_403_FORBIDDEN)
        
class EquipamentoPorTipoView(APIView):
    """
    Retorna a quantidade de equipamentos por tipo de equipamento de uma empresa
    """
    def get(self, request, pk):
        # Obtem a empresa com o id fornecido
        empresa = Empresa.objects.get(pk=pk)

        # Recupera a contagem de equipamentos por tipo de equipamento
        equipamentos_por_tipo = empresa.equipamento_set.values('tipo_equipamento__tipo').annotate(total=Count('tipo_equipamento__tipo'))

        # Formatando a resposta
        responde_data = [
            {'tipo': item['tipo_equipamento__tipo'], 'quantidade': item['total']} for item in equipamentos_por_tipo
        ]

        return Response(responde_data)

class EquipamentoPorStatusView(APIView):
    """
    Retorna a quantidade de equipamentos em cada status de uma empresa.
    """
    def get(self, request, pk):
        # Obtem a empresa com o id fornecido
        empresa = Empresa.objects.get(pk=pk)

        # Mapeando de status de numero para nome
        status_map = dict(SITUACAO_EQUIPAMENTO_CHOICES)
        
        # Recupera a contagem de equipamentos por situação
        equipamento_por_status = empresa.equipamento_set.values('situacao').annotate(total=Count('situacao'))

        # Substitui valores numericos pelos nomes
        for item in equipamento_por_status:
            item['status'] = status_map.get(item['situacao'], 'Desconhecido')

        # Formata a resposta
        response_data = [
            {'status': item['status'], 'quantidade': item['total']} for item in equipamento_por_status
        ]

        return Response(response_data)

class EquipamentoPorSetorView(APIView):
    """
    Retorna a quantidade de equipamentos por setor de uma empresa
    """
    def get(self, request, pk):
        # Obtém a empresa com o ID fornecido
        empresa = Empresa.objects.get(pk=pk)
        
        # Recupera a contagem de equipamentos por setor, excluindo equipamentos com setor nulo
        equipamentos_por_setor = empresa.equipamento_set.exclude(setor__isnull=True).values('setor__nome').annotate(total=Count('setor__nome'))
        
        # Conta os equipamentos sem setor
        equipamentos_sem_setor = empresa.equipamento_set.filter(setor__isnull=True).count()
        
        # Adiciona os equipamentos sem setor à contagem
        equipamentos_por_setor = list(equipamentos_por_setor)  # Converta para lista para ser mutável
        equipamentos_por_setor.append({'setor__nome': 'Sem Setor', 'total': equipamentos_sem_setor})
        
        # Formata a resposta
        response_data = [{'setor': item['setor__nome'] if item['setor__nome'] is not None else 'Sem Setor', 'quantidade': item['total']} for item in equipamentos_por_setor]
        
        return Response(response_data)

