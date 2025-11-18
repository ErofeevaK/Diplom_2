import pytest
import allure
from helpers import UserAPI

@pytest.fixture
def user_data():
    return UserAPI.generate_random_user()


@pytest.fixture
def registered_user(user_data):

    response = UserAPI.register(user_data)
    response_data = response.json()

    yield {
        'email': user_data['email'],
        'password': user_data['password'],
        'name': user_data['name'],
        'response': response,
        'response_data': response_data
    }

    # Очистка после теста
    UserAPI.delete_user(user_data)