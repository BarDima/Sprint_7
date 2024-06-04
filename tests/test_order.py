import allure
import pytest
import requests


url_get_orders = "https://qa-scooter.praktikum-services.ru/api/v1/orders?limit=10&page=0"
url = "https://qa-scooter.praktikum-services.ru/api/v1/orders"

test_data = [
    ({"color": ["BLACK"]}, 201),
    ({"color": ["BLACK", "GREY"]}, 201),
    ({}, 201)
]

class TestOrder:
    @pytest.mark.parametrize("color_payload, expected_status", test_data)
    @allure.title('Проверка возможности создания заказа')
    def test_create_order(self, color_payload, expected_status):
        order_data = {
            "firstName": "ivan",
            "lastName": "petrov",
            "address": "Odincova str., 23-12",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-06-06",
            "comment": "don't call the intercom"
        }
        order_data.update(color_payload)
        response = requests.post(url, json=order_data)
        assert response.status_code == expected_status
        response_json = response.json()
        assert "track" in response_json


    @allure.title('проверка, что в тело ответа возвращается список заказов')
    def test_get_orders(self):
        response = requests.get(url_get_orders)
        response_json = response.json()
        assert "orders" in response_json
        orders = response_json["orders"]
        assert isinstance(orders, list)
        assert len(orders) > 0



