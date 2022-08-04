
import unittest
import json

from inside24 import app

class Inside24TestCase(unittest.TestCase):

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    # Позитивный тест эндпоинта для проверки имени и пароля и генерации токена
    def test_login(self):
        response = self.client.post("/api/login", data=json.dumps({"name": "Admin", "password": "123456"}), content_type='application/json')
        assert response.status_code == 200
        assert "token" in response.get_json()

    # Негативный тест эндпоинта для проверки имени и пароля и генерации токена (неверные имя и пароль)
    def test_login_error_logpass(self):
        response = self.client.post("/api/login", data=json.dumps({"name": "admin", "password": "111222333"}), content_type='application/json')
        assert response.status_code == 200
        assert "ERROR" in response.get_json()['status']

    # Негативный тест эндпоинта для проверки имени и пароля и генерации токена (неверное имя)
    def test_login_error_log(self):
        response = self.client.post("/api/login", data=json.dumps({"name": "admin", "password": "123456"}), content_type='application/json')
        assert response.status_code == 200
        assert "ERROR" in response.get_json()['status']

    # Негативный тест эндпоинта для проверки имени и пароля и генерации токена (неверный пароль)
    def test_login_error_pass(self):
        response = self.client.post("/api/login", data=json.dumps({"name": "Admin", "password": "1234567"}), content_type='application/json')
        assert response.status_code == 200
        assert "ERROR" in response.get_json()['status']

    # Позитивный тест эндпоинта для получения сообщения пользователя и сохранения его в БД
    def test_message_save(self):
        response = self.client.post("/api/message", data=json.dumps({"name": "Client", "message": "My_text_message"}), headers={'Content-Type':'application/json', 'token': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiQ2xpZW50In0.X3mjhe_xUzD1PnrNMocVO-A6j9NZqy0s1AVsFMBFSN0'})
        assert response.status_code == 200
        assert "SUCCES" in response.get_json()['status']

    # Негативный тест эндпоинта для получения сообщения пользователя и сохранения его в БД (неверный токен)
    def test_message_save_error_tok(self):
        response = self.client.post("/api/message", data=json.dumps({"name": "Client", "message": "My_text_message"}), headers={'Content-Type':'application/json', 'token': 'Bearer_eyJ0eXAQiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiQ2xpZW50In0.X3mjhe_xUzD1PnrNMocVO-A6j9NZqy0s1AVsFMBFSN0'})
        assert response.status_code == 200
        assert "ERROR" in response.get_json()['status']

    # Негативный тест эндпоинта для получения сообщения пользователя и сохранения его в БД (неверное имя)
    def test_message_save_error_log(self):
        response = self.client.post("/api/message", data=json.dumps({"name": "other", "message": "My_text_message"}), headers={'Content-Type':'application/json', 'token': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiQ2xpZW50In0.X3mjhe_xUzD1PnrNMocVO-A6j9NZqy0s1AVsFMBFSN0'})
        assert response.status_code == 200
        assert "ERROR" in response.get_json()['status']

    # Позитивный тест эндпоинта для получения сообщения с командой вывода истории последних пользовательских сообщений
    def test_message_history(self):
        response = self.client.post("/api/message", data=json.dumps({"name": "Client", "message": "history 10"}), headers={'Content-Type':'application/json', 'token': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiQ2xpZW50In0.X3mjhe_xUzD1PnrNMocVO-A6j9NZqy0s1AVsFMBFSN0'})
        assert response.status_code == 200
        assert 10 <= len(response.get_json())
        assert "status" not in response.get_json()

    # Негативный тест эндпоинта для получения сообщения с командой вывода истории последних пользовательских сообщений (несуществующая команда, выполняется сохранение сообщения)
    def test_message_history_error_msg(self):
        response = self.client.post("/api/message", data=json.dumps({"name": "Client", "message": "my history 10"}), headers={'Content-Type':'application/json', 'token': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiQ2xpZW50In0.X3mjhe_xUzD1PnrNMocVO-A6j9NZqy0s1AVsFMBFSN0'})
        assert response.status_code == 200
        assert "SUCCESS" in response.get_json()['status']

    # Негативный тест эндпоинта для получения сообщения с командой вывода истории последних пользовательских сообщений (неверное)
    def test_message_history_error_log(self):
        response = self.client.post("/api/message", data=json.dumps({"name": "other", "message": "history 10"}), headers={'Content-Type':'application/json', 'token': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiQ2xpZW50In0.X3mjhe_xUzD1PnrNMocVO-A6j9NZqy0s1AVsFMBFSN0'})
        assert response.status_code == 200
        assert "ERROR" in response.get_json()['status']

if __name__ == "__main__":
    unittest.main()