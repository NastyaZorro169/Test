from django.contrib import admin
from .models import (
    Topic, Project, ProjectSettings, Task, TaskDetail,
    Subtask, Comment, Document, DocumentVersion, Template
)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'created_at', 'updated_at')
    list_filter = ('topic',)
    search_fields = ('name', 'description')

@admin.register(ProjectSettings)
class ProjectSettingsAdmin(admin.ModelAdmin):
    list_display = ('project', 'notification_enabled', 'created_at', 'updated_at')
    list_filter = ('notification_enabled',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'project')
    search_fields = ('title', 'description')

@admin.register(TaskDetail)
class TaskDetailAdmin(admin.ModelAdmin):
    list_display = ('task', 'created_at', 'updated_at')
    search_fields = ('requirements', 'acceptance_criteria')

@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'created_at')
    list_filter = ('status', 'task')
    search_fields = ('title', 'description')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'task', 'subtask', 'created_at')
    list_filter = ('author',)
    search_fields = ('content',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'task', 'created_at')
    list_filter = ('project', 'task')
    search_fields = ('title', 'content')

@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'version_number', 'created_by', 'created_at')
    list_filter = ('created_by',)
    search_fields = ('content',)

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'created_at', 'updated_at')
    list_filter = ('topic',)
    search_fields = ('name', 'content')
