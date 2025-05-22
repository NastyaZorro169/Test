from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TopicViewSet, ProjectViewSet, TaskViewSet,
    SubtaskViewSet, CommentViewSet, DocumentViewSet,
    DocumentVersionViewSet, TemplateViewSet, FavoriteViewSet,
    PredictDocumentClassView
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubtaskViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'document-versions', DocumentVersionViewSet)
router.register(r'templates', TemplateViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorite')

schema_view = get_schema_view(
    openapi.Info(
        title="UniDoc API",
        default_version='v1',
        description="API для системы UniDoc",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('predict-document-class/', PredictDocumentClassView.as_view(), name='predict-document-class'),
] 