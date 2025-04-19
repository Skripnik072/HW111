import json
import requests
from external_api import get_user_convert


def get_finans_tranz(path: str) -> dict:
    ''' Возвращает из JSON список словарей с финансовыми транзакциями'''
    my_list = []
    try:
        with open(path, encoding='utf-8') as finans_file:
            try:
                file_tranz = json.load(finans_file)
            except json.JSONDecodeError:
                print("Ошибка обработки кода")
                return my_list
    except FileNotFoundError:
        print("Файл не найден")
        return my_list
    return file_tranz


dict_tr = get_finans_tranz("date\\operations.json")
# print(dict_tr)

if __name__ == '__main__':
    get_finans_tranz("date\\operations.json")


def get_t_action_currency(tr_action: dict, amount=None) -> float:
    '''Функция принимает тразакцию и возвращет её сумму'''
    amount = ""
    amount_rub = 0.0
    for i in tr_action:
        if 'operationAmount' in i:
            if i["operationAmount"]["currency"]["code"] == "RUB":
                amount_rub = float(i["operationAmount"]["amount"])
#            return(amount_rub)
            elif i["operationAmount"]["currency"]["code"] == "USD":
                amount = float(i["operationAmount"]["amount"])
                amount_rub = get_user_convert(amount)
#            return(amount_rub)
        else:
            continue
    return (amount_rub)


amount_rub = get_t_action_currency(dict_tr)
print(f"Сумма транзакции {amount_rub} руб.")

