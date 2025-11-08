class ErrorMessages:
    REQUIRED_FIELDS = "Email, password and name are required fields"
    USER_EXISTS = "User already exists"
    INVALID_CREDENTIALS = "email or password are incorrect"
    UNAUTHORIZED_ACCESS = "You should be authorised"
    MISSING_INGREDIENTS = "Ingredient ids must be provided"
    INTERNAL_SERVER_ERROR = "Internal Server Error"


class AuthTestData:
    INVALID_LOGIN_DATA = [
        ({"email": "nonexistent@y.ru", "password": "wrongpassword"}, 401, ErrorMessages.INVALID_CREDENTIALS),
        ({"email": "", "password": "65498"}, 401, ErrorMessages.INVALID_CREDENTIALS),
        ({"email": "test_user@ya.ru", "password": ""}, 401, ErrorMessages.INVALID_CREDENTIALS),
        ({"password": "65498"}, 401, ErrorMessages.INVALID_CREDENTIALS),
        ({"email": "test_user"}, 401, ErrorMessages.INVALID_CREDENTIALS)
    ]


class IngredientsData:
    INGREDIENTS_DATA = ["61c0c5a71d1f82001bdaaa6f", "61c0c5a71d1f82001bdaaa71", "61c0c5a71d1f82001bdaaa74", "61c0c5a71d1f82001bdaaa78"]
    INVALID_HASH_INGREDIENT = ["61c0c5a71d1f82001bdaaq71"]