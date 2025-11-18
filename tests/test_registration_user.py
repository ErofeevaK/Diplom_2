import allure
import pytest

from helpers import UserAPI
from data import ErrorMessages


class TestRegistrationUser:
    @allure.title('Успешная регистрация пользователя')
    def test_registration_user_success(self):
     #Тест успешной регистрации пользователя
        with allure.step('Генерируем данные для нового пользователя'):
            user_data = UserAPI.generate_random_user()

        with allure.step('Регистрируем пользователя через API'):
            response = UserAPI.register(user_data)
            response_data = response.json()

        with allure.step('Проверяем успешную регистрацию'):
            assert response.status_code == 200
            assert response_data['success'] is True

        with allure.step('Очищаем данные: удаляем созданного пользователя'):
            UserAPI.delete_user(user_data)

    @allure.title('Попытка регистрации пользователя с уже существующими данными')
    def test_register_user_duplicate(self):

       #Тест регистрации пользователя с дублирующимися данными

        with allure.step('Генерируем данные и регистрируем первого пользователя'):
            user_data = UserAPI.generate_random_user()
            first_registration = UserAPI.register(user_data)
            assert first_registration.status_code == 200

        with allure.step('Попытка зарегистрировать пользователя с такими же данными'):
            duplicate_response = UserAPI.register(user_data)

        with allure.step('Проверяем ошибку дублирования'):
            assert duplicate_response.status_code == 403
            assert duplicate_response.json()['message'] == ErrorMessages.USER_EXISTS

        with allure.step('Очищаем данные: удаляем созданного пользователя'):
            UserAPI.delete_user(user_data)

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title('Попытка регистрации без обязательного поля {missing_field}')
    def test_registration_missing_field(self, missing_field):

        #Тест регистрации без обязательных полей

        with allure.step('Генерируем полные данные пользователя'):
            user_data = UserAPI.generate_random_user()

        with allure.step(f'Удаляем обязательное поле {missing_field}'):
            del user_data[missing_field]

        with allure.step(f'Попытка регистрации без поля {missing_field}'):
            response = UserAPI.register(user_data)

        with allure.step('Проверяем ответ сервера об ошибке'):
            assert response.status_code == 403
            assert response.json()['message'] == ErrorMessages.REQUIRED_FIELDS