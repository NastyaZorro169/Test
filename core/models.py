from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone

class TopicManager(models.Manager):
    def get_active_topics(self):
        """Получить темы с активными проектами"""
        return self.annotate(
            active_projects=Count('projects', filter=Q(projects__tasks__status__in=['new', 'in_progress']))
        ).filter(active_projects__gt=0)

class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TopicManager()

    def __str__(self):
        return self.name

    def get_active_projects_count(self):
        """Получить количество активных проектов"""
        return self.projects.filter(tasks__status__in=['new', 'in_progress']).distinct().count()

class ProjectManager(models.Manager):
    def get_projects_with_tasks_count(self):
        """Получить проекты с количеством задач"""
        return self.annotate(tasks_count=Count('tasks'))

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProjectManager()

    def __str__(self):
        return self.name

    def get_active_tasks_count(self):
        """Получить количество активных задач"""
        return self.tasks.filter(status__in=['new', 'in_progress']).count()

    def get_completed_tasks_count(self):
        """Получить количество завершенных задач"""
        return self.tasks.filter(status='done').count()

class ProjectSettings(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='settings')
    notification_enabled = models.BooleanField(default=True)
    template_default = models.ForeignKey('Template', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.project.name}"

class TaskManager(models.Manager):
    def get_tasks_by_status(self, status):
        """Получить задачи по статусу"""
        return self.filter(status=status)

    def get_overdue_tasks(self):
        """Получить просроченные задачи"""
        return self.filter(
            status__in=['new', 'in_progress'],
            created_at__lt=timezone.now() - timezone.timedelta(days=7)
        )

class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TaskManager()

    def __str__(self):
        return self.title

    def is_overdue(self):
        """Проверить, просрочена ли задача"""
        return (self.status in ['new', 'in_progress'] and 
                self.created_at < timezone.now() - timezone.timedelta(days=7))

    def get_subtasks_count(self):
        """Получить количество подзадач"""
        return self.subtasks.count()

    def get_comments_count(self):
        """Получить количество комментариев"""
        return self.comments.count()

class TaskDetail(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='details')
    requirements = models.TextField()
    acceptance_criteria = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Details for {self.task.title}"

class Subtask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=20, choices=Task.STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    subtask = models.ForeignKey(Subtask, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username}"

class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    content = models.TextField()
    version_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Version {self.version_number} of {self.document.title}"

class Template(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='favorited_by', null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='favorited_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('user', 'project'),
            ('user', 'task')
        ]

    def __str__(self):
        if self.project:
            return f"{self.user.username} favorited project {self.project.name}"
        return f"{self.user.username} favorited task {self.task.title}"
