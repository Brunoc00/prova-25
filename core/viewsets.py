from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone

from core.models import Task, Tag, TaskTag, User
# Importar serializers padrão
# Importar serializers customizados para requisições
from core.request_serializers import TaskCreateUpdateSerializer
from core.filters import TaskFilter, TagFilter
from core.serialiazers import TagSerializer, TaskDetailSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TagFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Tasks

    Endpoints disponíveis:
    - GET /api/tasks/ - Listar todas as tarefas
    - POST /api/tasks/ - Criar nova tarefa
    - GET /api/tasks/{id}/ - Detalhar tarefa
    - PUT /api/tasks/{id}/ - Atualizar tarefa completa
    - PATCH /api/tasks/{id}/ - Atualizar parcial
    - DELETE /api/tasks/{id}/ - Deletar tarefa
    - GET /api/tasks/my-tasks/ - Listar tarefas do usuário
    - POST /api/tasks/{id}/complete/ - Marcar como concluída
    """
    queryset = Task.objects.all().prefetch_related('tags')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'priority', 'due_date']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Usar serializer diferente para criar/atualizar"""
        if self.action in ['create', 'update', 'partial_update']:
            return TaskCreateUpdateSerializer
        return TaskDetailSerializer

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Endpoint para marcar uma tarefa como concluída

        POST /api/tasks/{id}/complete/
        """
        task = self.get_object()
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()

        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Listar todas as tarefas pendentes

        GET /api/tasks/pending/
        """
        tasks = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        Listar todas as tarefas concluídas

        GET /api/tasks/completed/
        """
        tasks = self.get_queryset().filter(status='completed')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)