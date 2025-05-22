from django.db import models
from django.core.cache import cache
from django.conf import settings
from django.db.models import Prefetch, Count, Q
from functools import wraps
import time

def cache_result(timeout=300):
    """
    Декоратор для кэширования результатов функций
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Создаем ключ кэша на основе аргументов функции
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            result = cache.get(cache_key)
            
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator

def query_timer(func):
    """
    Декоратор для измерения времени выполнения запросов
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Query time for {func.__name__}: {end_time - start_time:.2f} seconds")
        return result
    return wrapper

class TopicQuerySet(models.QuerySet):
    @query_timer
    def with_active_projects(self):
        """
        Оптимизированный запрос для получения тем с активными проектами
        """
        return self.annotate(
            active_projects_count=Count(
                'projects',
                filter=Q(projects__tasks__status__in=['new', 'in_progress']),
                distinct=True
            )
        ).filter(active_projects_count__gt=0)

    @query_timer
    def with_project_stats(self):
        """
        Оптимизированный запрос для получения тем со статистикой проектов
        """
        return self.annotate(
            total_projects=Count('projects'),
            active_projects=Count(
                'projects',
                filter=Q(projects__tasks__status__in=['new', 'in_progress']),
                distinct=True
            ),
            completed_projects=Count(
                'projects',
                filter=Q(projects__tasks__status='done'),
                distinct=True
            )
        )

class ProjectQuerySet(models.QuerySet):
    @query_timer
    def with_task_stats(self):
        """
        Оптимизированный запрос для получения проектов со статистикой задач
        """
        return self.annotate(
            total_tasks=Count('tasks'),
            active_tasks=Count(
                'tasks',
                filter=Q(tasks__status__in=['new', 'in_progress'])
            ),
            completed_tasks=Count(
                'tasks',
                filter=Q(tasks__status='done')
            )
        )

    @query_timer
    def with_related_data(self):
        """
        Оптимизированный запрос для получения проектов со связанными данными
        """
        return self.select_related('topic').prefetch_related(
            Prefetch(
                'tasks',
                queryset=Task.objects.select_related('assigned_to')
            ),
            'documents'
        )

class TaskQuerySet(models.QuerySet):
    @query_timer
    def with_related_data(self):
        """
        Оптимизированный запрос для получения задач со связанными данными
        """
        return self.select_related(
            'project',
            'project__topic',
            'assigned_to'
        ).prefetch_related(
            'subtasks',
            'comments',
            'documents'
        )

    @query_timer
    def with_subtask_stats(self):
        """
        Оптимизированный запрос для получения задач со статистикой подзадач
        """
        return self.annotate(
            total_subtasks=Count('subtasks'),
            completed_subtasks=Count(
                'subtasks',
                filter=Q(subtasks__status='done')
            )
        )

class DocumentQuerySet(models.QuerySet):
    @query_timer
    def with_versions(self):
        """
        Оптимизированный запрос для получения документов с версиями
        """
        return self.prefetch_related(
            Prefetch(
                'versions',
                queryset=DocumentVersion.objects.select_related('created_by')
            )
        )

# Оптимизированные менеджеры для моделей
class TopicManager(models.Manager):
    def get_queryset(self):
        return TopicQuerySet(self.model, using=self._db)

    @cache_result(timeout=300)
    def get_active_topics(self):
        return self.get_queryset().with_active_projects()

    @cache_result(timeout=300)
    def get_topics_with_stats(self):
        return self.get_queryset().with_project_stats()

class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

    @cache_result(timeout=300)
    def get_projects_with_stats(self):
        return self.get_queryset().with_task_stats()

    @cache_result(timeout=300)
    def get_projects_with_related(self):
        return self.get_queryset().with_related_data()

class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    @cache_result(timeout=300)
    def get_tasks_with_related(self):
        return self.get_queryset().with_related_data()

    @cache_result(timeout=300)
    def get_tasks_with_subtask_stats(self):
        return self.get_queryset().with_subtask_stats()

class DocumentManager(models.Manager):
    def get_queryset(self):
        return DocumentQuerySet(self.model, using=self._db)

    @cache_result(timeout=300)
    def get_documents_with_versions(self):
        return self.get_queryset().with_versions()

# Функции для массовых операций
def bulk_create_topics(topics_data):
    """
    Оптимизированное создание множества тем
    """
    topics = [Topic(**data) for data in topics_data]
    return Topic.objects.bulk_create(topics)

def bulk_create_projects(projects_data):
    """
    Оптимизированное создание множества проектов
    """
    projects = [Project(**data) for data in projects_data]
    return Project.objects.bulk_create(projects)

def bulk_create_tasks(tasks_data):
    """
    Оптимизированное создание множества задач
    """
    tasks = [Task(**data) for data in tasks_data]
    return Task.objects.bulk_create(tasks)

def bulk_create_documents(documents_data):
    """
    Оптимизированное создание множества документов
    """
    documents = [Document(**data) for data in documents_data]
    return Document.objects.bulk_create(documents) 