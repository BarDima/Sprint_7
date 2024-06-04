import allure
import requests
import random
import string


@allure.step('Генерируем строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки')
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

@allure.step('Регистрируем курьера, возвращаем логин, пароль, имя курьера')
def register_new_courier_and_return_login_password():
    # создаём список, чтобы метод мог его вернуть
    login_pass = []
    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass

@allure.step('Генерирум создание логина и пароля, возвращаем id курьера')
def login_and_get_courier_id(login, password):
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', json=payload)
    if response.status_code == 200:
        return response.json().get('id')
    return None

@allure.step('Удаляем курьера по id')
def delete_courier(courier_id):
    response = requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')
    return response.status_code






