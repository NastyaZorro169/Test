from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import (
    Topic, Project, Task, Subtask,
    Comment, Document, DocumentVersion, Template
)

class TopicAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.topic = Topic.objects.create(
            name="Test Topic",
            description="Test Description"
        )
        self.url = reverse('topic-list')

    def test_get_topics(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_topic(self):
        data = {
            'name': 'New Topic',
            'description': 'New Description'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Topic.objects.count(), 2)

    def test_get_topic_detail(self):
        url = reverse('topic-detail', args=[self.topic.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.topic.name)

class ProjectAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.topic = Topic.objects.create(name="Test Topic")
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            topic=self.topic
        )
        self.url = reverse('project-list')

    def test_get_projects(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_project(self):
        data = {
            'name': 'New Project',
            'description': 'New Description',
            'topic': self.topic.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_get_project_detail(self):
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.project.name)

class TaskAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.topic = Topic.objects.create(name="Test Topic")
        self.project = Project.objects.create(
            name="Test Project",
            topic=self.topic
        )
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            project=self.project,
            assigned_to=self.user
        )
        self.url = reverse('task-list')

    def test_get_tasks(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_task(self):
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'project': self.project.id,
            'assigned_to': self.user.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_get_task_detail(self):
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

class DocumentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
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
        self.url = reverse('document-list')

    def test_get_documents(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_document(self):
        data = {
            'title': 'New Document',
            'content': 'New Content',
            'project': self.project.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 2)

    def test_get_document_detail(self):
        url = reverse('document-detail', args=[self.document.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.document.title)

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.url = reverse('token_obtain_pair')

    def test_obtain_token(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        # First obtain token
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.url, data)
        refresh_token = response.data['refresh']

        # Then refresh it
        url = reverse('token_refresh')
        data = {'refresh': refresh_token}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data) 