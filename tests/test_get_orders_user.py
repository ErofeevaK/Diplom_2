import allure
import requests

from data import IngredientsData, ErrorMessages
from helpers import OrderAPI
from urls import Url

class TestGetOrdersUser:
    @allure.title('Тест на получение заказов конкретного авторизованного пользователя')
    def test_get_orders_for_specific_user(self, registered_user):
        with allure.step('Регистрируем пользователя, получаем данные из фикстуры'):
            user_data = registered_user
            access_token = user_data['access_token']

        with allure.step('Создаем заказ'):
            order_response = OrderAPI.create_order(registered_user, IngredientsData.INGREDIENTS_DATA)

            order_data = order_response.json()

        with allure.step('Формируем заголовок с токеном из фикстуры'):
            headers = {
                'Authorization': access_token
            }

        with allure.step('Получаем заказ'):
            get_orders_response = requests.get(Url.BASE_URL + Url.USER_GET_ORDERS_URL, headers=headers)

        assert get_orders_response.status_code == 200
        assert order_data['success'] is True


    @allure.title('Тест на получение заказов конкретного неавторизованного пользователя')
    def test_get_orders_for_user(self):

        with allure.step('Создаем заказ'):
            requests.post(Url.BASE_URL + Url.ORDER_CREATION_POST_URL, json={"ingredients": IngredientsData.INGREDIENTS_DATA})

        with allure.step('Формируем заголовок'):
            headers = {
                'Content-Type': 'application/json'
            }

        with allure.step('Получаем заказ'):
            get_orders_response = requests.get(Url.BASE_URL + Url.USER_GET_ORDERS_URL, headers=headers)

        assert get_orders_response.status_code == 401
        assert get_orders_response.json()['message'] == ErrorMessages.UNAUTHORIZED_ACCESS