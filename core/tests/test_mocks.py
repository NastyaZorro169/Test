from django.test import TestCase
from unittest.mock import Mock, patch
from ..models import Topic, Project, Task
from ..factories import TopicFactory, ProjectFactory, TaskFactory

class MockTest(TestCase):
    def setUp(self):
        self.topic = TopicFactory()
        self.project = ProjectFactory(topic=self.topic)
        self.task = TaskFactory(project=self.project)

    @patch('core.models.Topic.get_active_projects_count')
    def test_mock_active_projects(self, mock_count):
        mock_count.return_value = 5
        self.assertEqual(self.topic.get_active_projects_count(), 5)
        mock_count.assert_called_once()

    @patch('core.models.Project.get_active_tasks_count')
    def test_mock_active_tasks(self, mock_count):
        mock_count.return_value = 3
        self.assertEqual(self.project.get_active_tasks_count(), 3)
        mock_count.assert_called_once()

    @patch('core.models.Task.is_overdue')
    def test_mock_overdue_task(self, mock_overdue):
        mock_overdue.return_value = True
        self.assertTrue(self.task.is_overdue())
        mock_overdue.assert_called_once()

    @patch('core.models.Task.get_subtasks_count')
    def test_mock_subtasks_count(self, mock_count):
        mock_count.return_value = 4
        self.assertEqual(self.task.get_subtasks_count(), 4)
        mock_count.assert_called_once()

    @patch('core.models.Task.get_comments_count')
    def test_mock_comments_count(self, mock_count):
        mock_count.return_value = 2
        self.assertEqual(self.task.get_comments_count(), 2)
        mock_count.assert_called_once()