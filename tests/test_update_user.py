import allure
import requests

from urls import Url
from helpers import UserAPI
from data import ErrorMessages

class TestUpdateUser:
    @allure.title('Проверка изменения данных пользователя c авторизацией, проверем код и тело ответа')
    def test_update_user_success(self, registered_user):

        with allure.step('Получаем данные из фикстуры'):
            user_data = registered_user

        with allure.step('Генерируем новые данные для обновления (не регистрируем нового пользователя)'):
            new_data = {
                'email': f"updated_{user_data['email']}",
                'name': f"Updated {user_data['name']}"
            }

        with allure.step('Формируем заголовки с токеном из фикстуры'):
            headers = {
                'Authorization': user_data['access_token'],
                'Content-Type': 'application/json'
            }

        with allure.step('Отправляем запрос на обновление'):
            response = requests.patch(Url.BASE_URL + Url.USER_DATA_URL, headers=headers, json=new_data)

        with allure.step('Проверяем ответ'):
            response_data = response.json()

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert response_data['user']['email'] == new_data['email']
            assert response_data['user']['name'] == new_data['name']


    @allure.title('Проверка изменения данных пользователя без авторизации, система вернёт ошибку')
    def test_update_data_user_unauth_error(self):
        with allure.step("Генерация новых данных пользователя"):
            new_payload = UserAPI.generate_random_user()

        with allure.step("Подготовка заголовков для PATCH-запроса"):
            headers = {
                'Content-Type': 'application/json'
            }

        with allure.step("Выполнение PATCH-запроса на изменение данных пользователя без авторизации"):
            response = requests.patch(Url.BASE_URL + Url.USER_DATA_URL, headers=headers, json=new_payload)

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == 401
            assert response.json()['message'] == ErrorMessages.UNAUTHORIZED_ACCESS