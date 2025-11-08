import pytest

from helpers import UserAPI


@pytest.fixture(scope="function")
# Регистрирует пользователя
def registered_user():
    # Генерируем случайные данные пользователя
    user_data = UserAPI.generate_random_user()

    # Регистрируем пользователя и получаем объект ответа
    response = UserAPI.register(user_data)
    response_data = response.json()

    # Собираем и возвращаем итоговые данные
    yield {
        'email': user_data['email'],
        'password': user_data['password'],
        'name': user_data['name'],
        'access_token': response_data.get('accessToken'),
        'response': response,  # Сохраняем объект ответа
        'response_data': response_data  # Сохраняем распарсенные данные
    }

    # Удаляем пользователя
    UserAPI.delete_user(response_data.get('accessToken'))