from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from ..factories import UserFactory
from django.conf import settings
import time

class SeleniumTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = UserFactory(
            username='admin',
            is_staff=True,
            is_superuser=True
        )
        self.user.set_password('admin123')
        self.user.save()

    def test_admin_login(self):
        try:
            # Открываем страницу админки
            self.driver.get(f'{self.live_server_url}/api/admin/')
            time.sleep(2)  # Даем время на загрузку
            
            # Ждем загрузки формы
            username = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password = self.driver.find_element(By.NAME, "password")
            
            # Вводим учетные данные
            username.send_keys('admin')
            password.send_keys('admin123')
            
            # Нажимаем кнопку входа
            submit = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
            submit.click()
            
            # Проверяем, что мы вошли в админку
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "content-main"))
            )
            
            # Проверяем, что видим заголовок "Site administration"
            self.assertIn("Site administration", self.driver.page_source)
        except Exception as e:
            print(f"Error in test_admin_login: {str(e)}")
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source: {self.driver.page_source}")
            raise

    def test_swagger_ui(self):
        try:
            # Открываем Swagger UI
            self.driver.get(f'{self.live_server_url}/api/')
            time.sleep(2)  # Даем время на загрузку
            
            # Ждем загрузки Swagger UI
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swagger-ui"))
            )
            
            # Проверяем наличие основных эндпоинтов
            self.assertIn("topics", self.driver.page_source)
            self.assertIn("projects", self.driver.page_source)
            self.assertIn("tasks", self.driver.page_source)
        except Exception as e:
            print(f"Error in test_swagger_ui: {str(e)}")
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source: {self.driver.page_source}")
            raise