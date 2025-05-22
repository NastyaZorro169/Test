import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from .models import (
    Topic, Project, Task, Subtask,
    Comment, Document, DocumentVersion, Template
)

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class TopicFactory(DjangoModelFactory):
    class Meta:
        model = Topic

    name = factory.Sequence(lambda n: f'Topic {n}')
    description = factory.Faker('text')

class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: f'Project {n}')
    description = factory.Faker('text')
    topic = factory.SubFactory(TopicFactory)

class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Sequence(lambda n: f'Task {n}')
    description = factory.Faker('text')
    project = factory.SubFactory(ProjectFactory)
    assigned_to = factory.SubFactory(UserFactory)
    status = 'new'

class SubtaskFactory(DjangoModelFactory):
    class Meta:
        model = Subtask

    title = factory.Sequence(lambda n: f'Subtask {n}')
    description = factory.Faker('text')
    task = factory.SubFactory(TaskFactory)
    status = 'new'

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    content = factory.Faker('text')
    task = factory.SubFactory(TaskFactory)
    author = factory.SubFactory(UserFactory)

class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = Document

    title = factory.Sequence(lambda n: f'Document {n}')
    content = factory.Faker('text')
    project = factory.SubFactory(ProjectFactory)

class DocumentVersionFactory(DjangoModelFactory):
    class Meta:
        model = DocumentVersion

    document = factory.SubFactory(DocumentFactory)
    content = factory.Faker('text')
    version_number = factory.Sequence(lambda n: n)
    created_by = factory.SubFactory(UserFactory)

class TemplateFactory(DjangoModelFactory):
    class Meta:
        model = Template

    name = factory.Sequence(lambda n: f'Template {n}')
    content = factory.Faker('text')
    topic = factory.SubFactory(TopicFactory) 