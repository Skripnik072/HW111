import requests
from unittest.mock import patch, MagicMock
from src.external_api import get_user_convert

@patch("requests.get")
def test_get_user_convert(mock_request_get):
    # Создаем mock-ответ
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 10.5}
    # Пример корректного ответа API
    mock_request_get.return_value = mock_response
    # Проверяем, что функция возвращает то, что вернул бы response.json()
    assert get_user_convert("100") == {"result": 10.5}


@patch("requests.get")
def test_get_user_convert_cod400(mock_request_get):
    status_code = 400
    text = "error"
    mock_request_get.return_value.status_code = status_code
    mock_request_get.return_value.text = text
    assert get_user_convert("test") == \
        f"Ошибка при обращении к API {status_code} - {text}"
