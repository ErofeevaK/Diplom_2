import allure
import pytest

from helpers import UserAPI
from data import ErrorMessages

class TestRegistrationUser:
    @allure.title('Регистрация пользователя')
    def test_registration_user(self, registered_user):
        with allure.step('Проверка успешной регистрации пользователя: возвращает правильный код ответа - 200 и запрос возвращает {"success": true}'):

            assert registered_user['response'].status_code == 200
            assert registered_user['response_data']['success']

    @allure.title('Попытка регистрации пользователя с уже существующими данными')
    def test_register_user_duplicate(self, registered_user):
        with allure.step('Получаем логин и пароль из фикстуры'):
            duplicate_data = {
            'email': registered_user['email'],
            'password': registered_user['password'],
            'name': registered_user['name']
        }

        with allure.step('Попытка зарегистрировать пользователя с уже существующими данными'):
            response = UserAPI.register(duplicate_data)

        with allure.step('Проверка, что возвращается код ответа 403 и сообщение об ошибке'):

            assert response.status_code == 403
            assert response.json()['message'] == ErrorMessages.USER_EXISTS


    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title('Попытка регистрации без обязательного поля {missing_field}')
    def test_registration_missing_field(self, missing_field):
        with allure.step('Генерируем полные данные пользователя'):
            user_data = UserAPI.generate_random_user()

        with allure.step('Удаляем одно обязательное поле'):
            del user_data[missing_field]

        with allure.step(f'Попытка регистрации без поля {missing_field}'):
            response = UserAPI.register(user_data)

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == 403
            assert response.json()['message'] == ErrorMessages.REQUIRED_FIELDS