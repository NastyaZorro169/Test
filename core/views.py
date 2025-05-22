from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Topic, Project, ProjectSettings, Task, TaskDetail,
    Subtask, Comment, Document, DocumentVersion, Template,
    Favorite
)
from .serializers import (
    TopicSerializer, ProjectSerializer, TaskSerializer,
    SubtaskSerializer, CommentSerializer, DocumentSerializer,
    DocumentVersionSerializer, TemplateSerializer, FavoriteSerializer
)
from rest_framework.views import APIView
from rest_framework import status
import mlflow.pyfunc

# Create your views here.

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        queryset = Topic.objects.all()
        if self.request.query_params.get('active_only'):
            queryset = Topic.objects.get_active_topics()
        return queryset

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['topic', 'name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return Project.objects.get_projects_with_tasks_count()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'status', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'status', 'created_at']
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        queryset = Task.objects.all()
        status = self.request.query_params.get('status')
        if status:
            queryset = Task.objects.get_tasks_by_status(status)
        if self.request.query_params.get('overdue'):
            queryset = Task.objects.get_overdue_tasks()
        return queryset

class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['task', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'status', 'created_at']
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['task', 'subtask', 'author']
    search_fields = ['content']
    ordering_fields = ['created_at']
    http_method_names = ['get', 'post', 'put', 'delete']

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'task']
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'created_at']
    http_method_names = ['get', 'post', 'put', 'delete']

class DocumentVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['document', 'created_by']
    search_fields = ['content']
    ordering_fields = ['version_number', 'created_at']
    http_method_names = ['get']

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['topic']
    search_fields = ['name', 'content']
    ordering_fields = ['name', 'created_at']
    http_method_names = ['get', 'post', 'put', 'delete']

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['project', 'task']
    ordering_fields = ['created_at']
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PredictDocumentClassView(APIView):
    """
    API endpoint для предсказания класса документа по тексту.
    """
    def post(self, request):
        text = request.data.get('text')
        if not text:
            return Response({'error': 'Поле text обязательно.'}, status=status.HTTP_400_BAD_REQUEST)
        # Загружаем последнюю модель и векторизатор из MLflow
        model_uri = "models:/unidoc-document-tfidf-classification/Production"
        try:
            model = mlflow.pyfunc.load_model(model_uri)
        except Exception as e:
            return Response({'error': f'Ошибка загрузки модели: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Предсказываем класс
        try:
            prediction = model.predict([text])[0]
        except Exception as e:
            return Response({'error': f'Ошибка предсказания: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'prediction': int(prediction)})
