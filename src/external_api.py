import json
import requests


def get_user_convert(amount: str) -> str:
    '''Функция запрашивает курс для конвертации заданной валюты'''

    url = f"https://api.apilayer.com/exchangerates_data/convert?to=USD&from=RUB&amount={amount}"
    payload = {}
    headers = {
        'apikey': "clRtFIX4we3pMNXuluKfc26nNdY9LjoQ"
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    proba = response.status_code
    print(proba)
    if response.status_code != 200:
        return 'Ошибка при обращении к API 400 - error'
    return result


cur_result = get_user_convert("1000")
print(cur_result)
