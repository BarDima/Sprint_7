import allure
import requests
from helpers import register_new_courier_and_return_login_password
from helpers import generate_password_first_name
from helpers import generate_login_password_first_name
from helpers import login_and_get_courier_id
from helpers import delete_courier

url = "https://qa-scooter.praktikum-services.ru/api/v1/courier"
url_autorization = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'
class TestLoginCourier:

    @allure.title('Проверка возможности авторизации курьера')
    def test_authorization_courier(self):
        data = register_new_courier_and_return_login_password()
        login = data[0]
        password = data[1]
        courier_id = login_and_get_courier_id(login, password)
        assert courier_id
        delete_courier(courier_id)

    @allure.title('Проверка невозможности авторизации курьера с неверным паролем')
    def test_authorization_invalid_password_error(self):
        data = register_new_courier_and_return_login_password()
        payload = {
                "login": data[0],
                "password": "invalidpassword"
            }
        response = requests.post(url_autorization, json=payload)
        assert response.status_code == 404
        response_json = response.json()
        assert response_json.get("message") == "Учетная запись не найдена"
        courier_id = login_and_get_courier_id(data[0], data[1])
        delete_courier(courier_id)

    @allure.title('Проверка невозможности авторизации курьера с неверным логином')
    def test_authorization_invalid_login_error(self):
        data = register_new_courier_and_return_login_password()
        payload = {
                "login": "invalidlogin",
                "password": data[1]
            }
        response = requests.post(url_autorization, json=payload)
        assert response.status_code == 404
        response_json = response.json()
        assert response_json.get("message") == "Учетная запись не найдена"
        courier_id = login_and_get_courier_id(data[0], data[1])
        delete_courier(courier_id)

    @allure.title('Проверка невозможности авторизации курьера с пустым полем пароля')
    def test_authorization_without_password_error(self):
        data = register_new_courier_and_return_login_password()
        payload = {
                "login": data[0],
                "password": ''
            }
        response = requests.post(url_autorization, json=payload)
        assert response.status_code == 400
        response_json = response.json()
        assert response_json.get("message") == "Недостаточно данных для входа"
        courier_id = login_and_get_courier_id(data[0], data[1])
        delete_courier(courier_id)

    @allure.title('Проверка невозможности авторизации курьера с пустым полем login')
    def test_authorization_without_login_error(self):
        data = register_new_courier_and_return_login_password()
        payload = {
                "login": '',
                "password": data[1]
            }
        response = requests.post(url_autorization, json=payload)
        assert response.status_code == 400
        response_json = response.json()
        assert response_json.get("message") == "Недостаточно данных для входа"
        courier_id = login_and_get_courier_id(data[0], data[1])
        delete_courier(courier_id)

    @allure.title('Проверка невозможности авторизации незарегистрированного курьера')
    def test_authorization_invalid_login_password_error(self):
        data = register_new_courier_and_return_login_password()
        payload = {
                "login": "invalidlogin",
                "password": "invalidpassword"
            }
        response = requests.post(url_autorization, json=payload)
        assert response.status_code == 404
        response_json = response.json()
        assert response_json.get("message") == "Учетная запись не найдена"
        courier_id = login_and_get_courier_id(data[0], data[1])
        delete_courier(courier_id)
