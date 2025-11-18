import allure
import requests
import pytest

from urls import Url
from data import AuthTestData


class TestLoginUser:
    @allure.title('Авторизация пользователя')
    def test_login_user(self, registered_user):
        with allure.step("Получаем логин и пароль из фикстуры"):
            login_data = {
            'email': registered_user['email'],
            'password': registered_user['password'],
            'name': registered_user['name']
        }

        with allure.step("Авторизация пользователя"):
            response = requests.post(Url.BASE_URL + Url.USER_LOGIN_URL, json=login_data)
            response_data = response.json()

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == 200
            assert response_data['success']

    @pytest.mark.parametrize("login_data, expected_status_code, expected_message", AuthTestData.INVALID_LOGIN_DATA)
    @allure.title('Проверка негативных сценариев авторизации пользователя')
    def test_login_user_negative(self, login_data, expected_status_code, expected_message):
        with allure.step("Авторизация пользователя"):
            response = requests.post(Url.BASE_URL + Url.USER_LOGIN_URL, json=login_data)

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == expected_status_code
            assert response.json().get("message") == expected_message