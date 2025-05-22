import os
import mlflow

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5001"))
# Инициализация Django для standalone-скрипта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unidoc.settings")
import django
django.setup()

import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from core.models import DocumentVersion


def load_data():
    """
    Загружает данные из DocumentVersion и формирует признаки и метки.
    Признак: TF-IDF по тексту версии.
    Метка: id проекта документа (или 0, если нет проекта).
    """
    versions = DocumentVersion.objects.select_related('document').all()
    if not versions.exists():
        print("В базе нет версий документов. Сгенерируйте тестовые данные!")
        return None, None
    texts = []
    labels = []
    for v in versions:
        texts.append(v.content)
        # Метка — id проекта, если есть, иначе 0
        labels.append(v.document.project.id if v.document and v.document.project else 0)
    return texts, np.array(labels)

def train_model(X_texts, y):
    """
    Обработка текста через TF-IDF, обучение модели классификации.
    """
    vectorizer = TfidfVectorizer(max_features=300)
    X = vectorizer.fit_transform(X_texts)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return model, vectorizer, accuracy, report

if __name__ == "__main__":
    # Настройка MLflow
    mlflow.set_tracking_uri("http://localhost:5001")
    mlflow.set_experiment("unidoc-document-tfidf-classification")

    # Загрузка данных
    X_texts, y = load_data()
    if X_texts is None or y is None:
        print("Нет данных для обучения. Завершение работы.")
        exit(1)

    # Тренировка модели и логирование в MLflow
    with mlflow.start_run():
        model, vectorizer, accuracy, report = train_model(X_texts, y)
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("vectorizer", "tfidf")
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model")
        mlflow.sklearn.log_model(vectorizer, "vectorizer")
        print(f"Точность модели: {accuracy:.3f}")
        print("Classification report:\n", report)
        print("Эксперимент успешно залогирован в MLflow!") 