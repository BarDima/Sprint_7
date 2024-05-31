import allure
import requests
from helpers import register_new_courier_and_return_login_password
from helpers import generate_password_first_name
from helpers import generate_login_password_first_name
from helpers import login_and_get_courier_id
from helpers import delete_courier

url = "https://qa-scooter.praktikum-services.ru/api/v1/courier"
url_autorization = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'
class TestCourier:

    @allure.title('Проверка возможности создания курьера')
    def test_create_courier(self):
        data = generate_login_password_first_name()
        response = requests.post(url, json=data)
        assert response.status_code == 201
        assert response.json().get("ok") == True
        courier_id = login_and_get_courier_id(data['login'], data['password'])
        delete_courier(courier_id)

    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    def test_duplicate_courier_registration_error(self):
        data = register_new_courier_and_return_login_password()
        response = requests.post(url, json={
        "login": data[0],
        "password": data[1],
        "firstName": data[2]
    })
        assert response.status_code == 409
        courier_id = login_and_get_courier_id(data[0], data[1])
        delete_courier(courier_id)

    @allure.title('Проверка невозможности создания курьера без передачи поля логин')
    def test_create_courier_without_login_error(self):
        data = generate_password_first_name()
        response = requests.post(url, json=data)
        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.json().get("message")








