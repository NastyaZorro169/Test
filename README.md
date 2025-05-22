# UniDoc + MLflow: Интеллектуальная платформа документооборота

## Структура проекта

```
.
├── core/                # Основное Django-приложение
│   ├── models.py        # Модели данных
│   ├── views.py         # API, включая ML endpoint
│   ├── urls.py          # Маршруты
│   └── ...
├── unidoc/              # Django настройки
├── deploy/mlflow/       # MLflow + Postgres (Docker Compose)
│   ├── docker-compose.yml
│   └── Dockerfile
├── terraform/           # Инфраструктура Yandex Cloud (S3)
│   ├── modules/bucket/  # Модуль для создания S3 бакета
│   └── envs/dev/        # Конфигурация для dev окружения
├── unidoc/ml/           # ML-эксперименты (train.py)
├── requirements.txt     # Python-зависимости
└── .github/workflows/   # CI/CD pipeline
```

## Требования

- Python 3.11+
- Docker и Docker Compose
- Terraform 1.0+
- Yandex Cloud CLI (опционально)

## Настройка окружения

1. **Создайте `.env` файл в корне проекта:**
   ```env
   DB_NAME=mlflow
   DB_USER=mlflow
   DB_PASSWORD=changeme
   DB_HOST=localhost
   DB_PORT=5432
   AWS_ACCESS_KEY_ID=ваш_s3_key
   AWS_SECRET_ACCESS_KEY=ваш_s3_secret
   ```

2. **Настройте GitHub Secrets для CI/CD:**
   - `YC_KEY`: Yandex Cloud API ключ
   - `YC_S3_KEY`: Access key для Yandex Object Storage
   - `YC_S3_SECRET`: Secret key для Yandex Object Storage

## Развертывание инфраструктуры

1. **Инициализация Terraform:**
   ```bash
   cd terraform/envs/dev
   terraform init
   ```

2. **Применение конфигурации:**
   ```bash
   terraform apply
   ```

## Запуск MLflow

1. **Запуск MLflow и Postgres:**
   ```bash
   cd deploy/mlflow
   docker-compose up -d --build
   ```
   MLflow будет доступен на http://localhost:5001

## Разработка

1. **Установка зависимостей:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Миграции базы данных:**
   ```bash
   python manage.py migrate
   ```

3. **Генерация тестовых данных:**
   ```bash
   python manage.py shell -c "from core.management.commands.generate_test_data import Command; Command().handle()"
   ```

4. **Запуск обучения ML-модели:**
   ```bash
   PYTHONPATH=$(pwd) python unidoc/ml/train.py
   ```

## CI/CD Pipeline

Pipeline состоит из трех этапов:

1. **Infra**: Создание S3 бакета в Yandex Cloud
2. **Deploy**: Развертывание MLflow и Postgres
3. **Test ML**: Обучение и тестирование ML-модели

## MLflow в проекте

MLflow используется для:
- Отслеживания экспериментов с ML моделями
- Сохранения метрик и параметров моделей
- Хранения артефактов (моделей) в S3
- Предоставления UI для анализа результатов

## API Endpoints

- Swagger UI: `/api/`
- ReDoc: `/api/redoc/`
- ML Prediction: POST `/api/predict-document-class/`

## Безопасность

- Все секреты хранятся в GitHub Secrets
- Локальные секреты в `.env` (не коммитятся в git)
- Используется HTTPS в production
- JWT аутентификация для API

## Мониторинг и логирование

- MLflow UI для мониторинга ML экспериментов
- Django logging для приложения
- Terraform state в Yandex Cloud

## Дальнейшие улучшения

1. Добавление мониторинга через Prometheus/Grafana
2. Интеграция с BERT/transformers для улучшения классификации
3. Автоматическое масштабирование MLflow
4. Добавление тестов для ML компонентов

## Важно: переменные окружения для Terraform и CI/CD

Для корректной работы пайплайна и Terraform необходимо задать значения переменных:
- `cloud_id` — идентификатор облака Yandex Cloud
- `folder_id` — идентификатор каталога Yandex Cloud

### Как задать переменные:

**Вариант 1: через GitHub Secrets**
1. В настройках репозитория GitHub перейдите в Settings → Secrets and variables → Actions.
2. Добавьте секреты:
   - `YC_CLOUD_ID` — ваш cloud_id
   - `YC_FOLDER_ID` — ваш folder_id
3. В workflow (`.github/workflows/ci.yml`) добавьте их в секцию `env` для job `infra`:
   ```yaml
   env:
     YC_KEY: ${{ secrets.YC_KEY }}
     YC_S3_KEY: ${{ secrets.YC_S3_KEY }}
     YC_S3_SECRET: ${{ secrets.YC_S3_SECRET }}
     YC_CLOUD_ID: ${{ secrets.YC_CLOUD_ID }}
     YC_FOLDER_ID: ${{ secrets.YC_FOLDER_ID }}
   ```
4. В файле `terraform/envs/dev/main.tf` убедитесь, что используется:
   ```hcl
   provider "yandex" {
     token     = var.yc_token
     cloud_id  = var.cloud_id
     folder_id = var.folder_id
     zone      = var.zone
   }
   ```

**Вариант 2: через файл terraform.tfvars**

В файле `terraform/envs/dev/terraform.tfvars` добавьте:
```hcl
cloud_id  = "ваш_cloud_id"
folder_id = "ваш_folder_id"
```

## Быстрый старт (локально)

1. **Создайте файл `.env` в корне:**
   ```env
   DB_NAME=mlflow
   DB_USER=mlflow
   DB_PASSWORD=changeme
   DB_HOST=localhost
   DB_PORT=5432
   AWS_ACCESS_KEY_ID=ваш_s3_key
   AWS_SECRET_ACCESS_KEY=ваш_s3_secret
   ```

2. **Запустите Postgres и MLflow:**
   ```bash
   cd deploy/mlflow
   docker-compose up -d --build
   ```

3. **Выполните миграции и сгенерируйте тестовые данные:**
   ```bash
   python manage.py migrate
   python manage.py shell -c "from core.management.commands.generate_test_data import Command; Command().handle()"
   ```

4. **Запустите обучение ML-модуля:**
   ```bash
   PYTHONPATH=$(pwd) python unidoc/ml/train.py
   ```

## CI/CD Pipeline

- **infra**: применяет Terraform, создаёт S3 бакет
- **deploy**: поднимает MLflow (docker-compose)
- **test-ml**: устанавливает зависимости, запускает обучение

### Важно!
- В job test-ml MLflow должен быть добавлен как сервис через секцию `services` (см. ниже).
- Все переменные для S3 должны быть заданы через GitHub Secrets.

## Минимальный рабочий сервис MLflow для теста (CI/CD)

В секции `test-ml` вашего `.github/workflows/ci.yml` добавьте:

```yaml
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.10.2
    ports:
      - 5001:5000
    env:
      BACKEND_STORE_URI: sqlite:///mlflow.db
    options: >-
      --health-cmd "curl --fail http://localhost:5000/ || exit 1"
      --health-interval 5s
      --health-timeout 2s
      --health-retries 10
```

Если сервис стартует — добавляйте по одной переменной (ARTIFACT_ROOT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) и проверяйте, на какой падает.

## Типовые ошибки и их решение

- **MLflow не стартует как сервис** — проверь переменные окружения, попробуй запустить только с `BACKEND_STORE_URI: sqlite:///mlflow.db` (см. выше).
- **Django не видит базу** — проверь, что Postgres запущен, и параметры в `.env` совпадают с `docker-compose.yml`.
- **train.py не видит MLflow** — убедись, что MLflow стартует как сервис в job test-ml, и порт совпадает (`5000` внутри контейнера, `5001` снаружи).

## Пример секции services для MLflow в GitHub Actions (полная)

```yaml
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.10.2
    ports:
      - 5001:5000
    env:
      BACKEND_STORE_URI: sqlite:///mlflow.db
      ARTIFACT_ROOT: s3://mlflowtuesday-artifacts/artifacts
      AWS_ACCESS_KEY_ID: ${{ secrets.YC_S3_KEY }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.YC_S3_SECRET }}
    options: >-
      --health-cmd "curl --fail http://localhost:5000/ || exit 1"
      --health-interval 5s
      --health-timeout 2s
      --health-retries 10
```

## Переменные окружения для CI/CD

- Все секреты (ключи, токены) должны быть заданы через GitHub Secrets.
- Для MLflow и S3:
  - `YC_S3_KEY` — Access key для Yandex Object Storage
  - `YC_S3_SECRET` — Secret key для Yandex Object Storage

## Пример запуска обучения в CI/CD

```yaml
- name: Run ML Training
  env:
    MLFLOW_TRACKING_URI: http://localhost:5000
    AWS_ACCESS_KEY_ID: ${{ secrets.YC_S3_KEY }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.YC_S3_SECRET }}
  run: |
    PYTHONPATH=$(pwd) python unidoc/ml/train.py
```

---

**Если сервис MLflow не стартует — смотри логи контейнера в Actions или пробуй минимальную конфигурацию (см. выше).**

