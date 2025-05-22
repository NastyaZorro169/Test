from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Topic, Project, ProjectSettings, Task, TaskDetail, Subtask, Comment, Document, DocumentVersion, Template
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Генерирует тестовые данные для CRM системы авиакомпании'

    def handle(self, *args, **kwargs):
        # Создаем суперпользователя, если его нет
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Создан суперпользователь admin/admin123')

        # Создаем обычных пользователей
        users = []
        for i in range(3):
            username = f'user{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, f'{username}@example.com', 'password123')
                users.append(user)
                self.stdout.write(f'Создан пользователь {username}/password123')

        # Создаем тему
        topic = Topic.objects.create(
            name='CRM Система Авиакомпании',
            description='Разработка и внедрение CRM системы для управления клиентами авиакомпании'
        )
        self.stdout.write('Создана тема: CRM Система Авиакомпании')

        # Создаем шаблоны
        templates = [
            Template.objects.create(
                name='Шаблон требования',
                content='''# Требования к функционалу
## Описание
{description}
## Критерии приемки
{criteria}''',
                topic=topic
            ),
            Template.objects.create(
                name='Шаблон документации',
                content='''# Документация
## Назначение
{purpose}
## Структура
{structure}''',
                topic=topic
            )
        ]
        self.stdout.write('Созданы шаблоны документов')

        # Создаем проекты
        projects = [
            Project.objects.create(
                name='Анализ требований',
                description='Сбор и анализ требований к CRM системе',
                topic=topic
            ),
            Project.objects.create(
                name='Разработка модуля бронирования',
                description='Разработка модуля для управления бронированиями',
                topic=topic
            ),
            Project.objects.create(
                name='Интеграция с платежными системами',
                description='Интеграция CRM с платежными системами',
                topic=topic
            )
        ]
        self.stdout.write('Созданы проекты')

        # Создаем настройки проектов
        for project in projects:
            ProjectSettings.objects.create(
                project=project,
                notification_enabled=True,
                template_default=random.choice(templates)
            )
        self.stdout.write('Созданы настройки проектов')

        # Создаем задачи
        tasks = []
        for project in projects:
            project_tasks = [
                Task.objects.create(
                    title=f'Задача {i+1} для {project.name}',
                    description=f'Описание задачи {i+1} для проекта {project.name}',
                    project=project,
                    status=random.choice(['new', 'in_progress', 'review', 'done']),
                    assigned_to=random.choice(users) if users else None
                )
                for i in range(3)
            ]
            tasks.extend(project_tasks)
        self.stdout.write('Созданы задачи')

        # Создаем детали задач
        for task in tasks:
            TaskDetail.objects.create(
                task=task,
                requirements=f'Требования для задачи {task.title}',
                acceptance_criteria=f'Критерии приемки для задачи {task.title}'
            )
        self.stdout.write('Созданы детали задач')

        # Создаем подзадачи
        for task in tasks:
            for i in range(2):
                Subtask.objects.create(
                    title=f'Подзадача {i+1} для {task.title}',
                    description=f'Описание подзадачи {i+1} для задачи {task.title}',
                    task=task,
                    status=random.choice(['new', 'in_progress', 'review', 'done'])
                )
        self.stdout.write('Созданы подзадачи')

        # Создаем комментарии
        for task in tasks:
            for i in range(2):
                Comment.objects.create(
                    content=f'Комментарий {i+1} к задаче {task.title}',
                    task=task,
                    author=random.choice(users) if users else None
                )
        self.stdout.write('Созданы комментарии')

        # Создаем документы
        documents = []
        for project in projects:
            doc = Document.objects.create(
                title=f'Документация проекта {project.name}',
                content=f'Содержание документации проекта {project.name}',
                project=project
            )
            documents.append(doc)
        self.stdout.write('Созданы документы')

        # Создаем версии документов
        for doc in documents:
            for i in range(2):
                DocumentVersion.objects.create(
                    document=doc,
                    content=f'Версия {i+1} документа {doc.title}',
                    version_number=i+1,
                    created_by=random.choice(users) if users else None
                )
        self.stdout.write('Созданы версии документов')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!')) 