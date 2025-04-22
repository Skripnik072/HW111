import requests


def get_user_convert(amount: str, currency: str) -> str:
    '''Функция запрашивает курс для конвертации заданной валюты'''

    url = f"https://api.apilayer.com/exchangerates_data/convert?to=USD&from=RUB&amount=1000"
    payload = {}
    headers = {
        'apikey': "clRtFIX4we3pMNXuluKfc26nNdY9LjoQ"
    }
    response = requests.get(url, headers=headers, timeout=5)
    status_code = response.status_code
    print(response.status_code)
    if status_code == 200:
        result = response.json()
        return result
    else:
        return 'Ошибка при обращении к API 400 - error'


# cur_result = get_user_convert("1000", "USD")
# print(cur_result)
