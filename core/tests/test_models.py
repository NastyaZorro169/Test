from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import (
    Topic, Project, Task, Subtask,
    Comment, Document, DocumentVersion, Template
)

class TopicModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            name="Test Topic",
            description="Test Description"
        )

    def test_topic_creation(self):
        self.assertEqual(self.topic.name, "Test Topic")
        self.assertEqual(self.topic.description, "Test Description")
        self.assertTrue(isinstance(self.topic, Topic))
        self.assertEqual(str(self.topic), self.topic.name)

    def test_get_active_projects_count(self):
        self.assertEqual(self.topic.get_active_projects_count(), 0)

class ProjectModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            topic=self.topic
        )

    def test_project_creation(self):
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.description, "Test Description")
        self.assertEqual(self.project.topic, self.topic)
        self.assertTrue(isinstance(self.project, Project))
        self.assertEqual(str(self.project), self.project.name)

    def test_get_active_tasks_count(self):
        self.assertEqual(self.project.get_active_tasks_count(), 0)

    def test_get_completed_tasks_count(self):
        self.assertEqual(self.project.get_completed_tasks_count(), 0)

class TaskModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.project = Project.objects.create(
            name="Test Project",
            topic=self.topic
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            project=self.project,
            assigned_to=self.user
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "Test Description")
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.assigned_to, self.user)
        self.assertEqual(self.task.status, 'new')
        self.assertTrue(isinstance(self.task, Task))
        self.assertEqual(str(self.task), self.task.title)

    def test_is_overdue(self):
        self.assertFalse(self.task.is_overdue())

    def test_get_subtasks_count(self):
        self.assertEqual(self.task.get_subtasks_count(), 0)

    def test_get_comments_count(self):
        self.assertEqual(self.task.get_comments_count(), 0)

class SubtaskModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.project = Project.objects.create(
            name="Test Project",
            topic=self.topic
        )
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            project=self.project
        )
        self.subtask = Subtask.objects.create(
            title="Test Subtask",
            description="Test Description",
            task=self.task
        )

    def test_subtask_creation(self):
        self.assertEqual(self.subtask.title, "Test Subtask")
        self.assertEqual(self.subtask.description, "Test Description")
        self.assertEqual(self.subtask.task, self.task)
        self.assertEqual(self.subtask.status, 'new')
        self.assertTrue(isinstance(self.subtask, Subtask))
        self.assertEqual(str(self.subtask), self.subtask.title)

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.topic = Topic.objects.create(name="Test Topic")
        self.project = Project.objects.create(
            name="Test Project",
            topic=self.topic
        )
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            project=self.project
        )
        self.comment = Comment.objects.create(
            content="Test Comment",
            task=self.task,
            author=self.user
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, "Test Comment")
        self.assertEqual(self.comment.task, self.task)
        self.assertEqual(self.comment.author, self.user)
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertEqual(str(self.comment), f"Comment by {self.user.username}")

class DocumentModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.project = Project.objects.create(
            name="Test Project",
            topic=self.topic
        )
        self.document = Document.objects.create(
            title="Test Document",
            content="Test Content",
            project=self.project
        )

    def test_document_creation(self):
        self.assertEqual(self.document.title, "Test Document")
        self.assertEqual(self.document.content, "Test Content")
        self.assertEqual(self.document.project, self.project)
        self.assertTrue(isinstance(self.document, Document))
        self.assertEqual(str(self.document), self.document.title)

class DocumentVersionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.topic = Topic.objects.create(name="Test Topic")
        self.project = Project.objects.create(
            name="Test Project",
            topic=self.topic
        )
        self.document = Document.objects.create(
            title="Test Document",
            content="Test Content",
            project=self.project
        )
        self.version = DocumentVersion.objects.create(
            document=self.document,
            content="Test Version Content",
            version_number=1,
            created_by=self.user
        )

    def test_version_creation(self):
        self.assertEqual(self.version.document, self.document)
        self.assertEqual(self.version.content, "Test Version Content")
        self.assertEqual(self.version.version_number, 1)
        self.assertEqual(self.version.created_by, self.user)
        self.assertTrue(isinstance(self.version, DocumentVersion))
        self.assertEqual(str(self.version), f"Version {self.version.version_number} of {self.document.title}")

class TemplateModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.template = Template.objects.create(
            name="Test Template",
            content="Test Content",
            topic=self.topic
        )

    def test_template_creation(self):
        self.assertEqual(self.template.name, "Test Template")
        self.assertEqual(self.template.content, "Test Content")
        self.assertEqual(self.template.topic, self.topic)
        self.assertTrue(isinstance(self.template, Template))
        self.assertEqual(str(self.template), self.template.name) 