import allure
import requests

from data import IngredientsData, ErrorMessages
from helpers import OrderAPI
from urls import Url


class TestCreateOrderWithAuth:
    @allure.title('Тест успешного создания заказа авторизованного пользователя с ингредиентами')
    def test_create_order_with_ingredients_success(self, registered_user):
        with allure.step("Создаем заказ с ингредиентами"):
            response = OrderAPI.create_order(registered_user, IngredientsData.INGREDIENTS_DATA)

        with allure.step("Парсим JSON-ответ"):
            response_data = response.json()

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert 'name' in response_data
            assert 'order' in response_data
            assert 'number' in response_data['order']


    @allure.title('Тест создания заказа авторизованного пользователя без ингредиентов, возвращает 400')
    def test_create_order_without_ingredients_fails(self, registered_user):
        with allure.step("Создаем заказ без ингредиентов"):
            response = OrderAPI.create_order(registered_user, [])

        with allure.step("Парсим JSON-ответ"):
            response_data = response.json()

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == 400
            assert response_data['success'] is False
            assert response_data['message'] == ErrorMessages.MISSING_INGREDIENTS


    @allure.title('Тест создания заказа авторизованного пользователя с невалидным хешем ингредиента, возвращает 500')
    def test_create_order_with_invalid_hash_fails(self, registered_user):
        with allure.step("Создаем заказ с невалидным хешем ингредиента"):
            response = OrderAPI.create_order(registered_user, IngredientsData.INVALID_HASH_INGREDIENT)

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == 500
            assert ErrorMessages.INTERNAL_SERVER_ERROR in response.text



class TestCreateOrderUnAuth:
    @allure.title('Тест успешного создания заказа без авторизации, с ингредиентами ')
    def test_create_order_unauthorized_fails(self):
        with allure.step("Создаем заказ без авторизации, с ингредиентами"):
            response = requests.post(Url.BASE_URL + Url.ORDER_CREATION_POST_URL, json={"ingredients": IngredientsData.INGREDIENTS_DATA})

            response_data = response.json()

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == 200
            assert response_data['success'] is True


    @allure.title('Тест создания заказа без авторизации, без ингредиентов')
    def test_create_order_unauthorized_without_ingredients_fails(self):
        with allure.step("Создаем заказ без авторизации, без ингредиентов"):
            response = requests.post(Url.BASE_URL + Url.ORDER_CREATION_POST_URL, json={"ingredients": []})

            response_data = response.json()

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == 400
            assert response_data['success'] is False
            assert response_data['message'] == ErrorMessages.MISSING_INGREDIENTS


    @allure.title('Тест создания заказа без авторизации, с невалидным хешем ингредиента')
    def test_create_order_unauthorized_invalid_hash_fails(self):
        with allure.step("Создаем заказ без авторизации, с невалидным хешем ингредиента"):
            response = requests.post(Url.BASE_URL + Url.ORDER_CREATION_POST_URL, json={"ingredients": IngredientsData.INVALID_HASH_INGREDIENT})

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == 500
            assert ErrorMessages.INTERNAL_SERVER_ERROR in response.text