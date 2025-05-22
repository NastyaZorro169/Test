from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Topic, Project, ProjectSettings, Task, TaskDetail,
    Subtask, Comment, Document, DocumentVersion, Template,
    Favorite
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TopicSerializer(serializers.ModelSerializer):
    active_projects_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'active_projects_count']

    def get_active_projects_count(self, obj):
        return obj.get_active_projects_count()

class ProjectSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSettings
        fields = ['id', 'notification_enabled', 'template_default']

class ProjectSerializer(serializers.ModelSerializer):
    settings = ProjectSettingsSerializer(read_only=True)
    active_tasks_count = serializers.SerializerMethodField()
    completed_tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'topic', 'settings', 
                 'active_tasks_count', 'completed_tasks_count', 
                 'created_at', 'updated_at']

    def get_active_tasks_count(self, obj):
        return obj.get_active_tasks_count()

    def get_completed_tasks_count(self, obj):
        return obj.get_completed_tasks_count()

class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDetail
        fields = ['id', 'requirements', 'acceptance_criteria']

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'updated_at']

class TaskSerializer(serializers.ModelSerializer):
    details = TaskDetailSerializer(read_only=True)
    subtasks = SubtaskSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    assigned_to = UserSerializer(read_only=True)
    is_overdue = serializers.SerializerMethodField()
    subtasks_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'status',
                 'assigned_to', 'details', 'subtasks', 'comments',
                 'is_overdue', 'subtasks_count', 'comments_count',
                 'created_at', 'updated_at']

    def get_is_overdue(self, obj):
        return obj.is_overdue()

    def get_subtasks_count(self, obj):
        return obj.get_subtasks_count()

    def get_comments_count(self, obj):
        return obj.get_comments_count()

class DocumentVersionSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = DocumentVersion
        fields = ['id', 'content', 'version_number', 'created_by', 'created_at']

class DocumentSerializer(serializers.ModelSerializer):
    versions = DocumentVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'project', 'task', 'versions',
                 'created_at', 'updated_at']

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'name', 'content', 'topic', 'created_at', 'updated_at']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'project', 'task', 'created_at']
        read_only_fields = ['user', 'created_at'] 