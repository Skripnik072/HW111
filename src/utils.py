import json
import os
from src.external_api import get_user_convert


def get_finans_tranz(path: str) -> dict:
    ''' Возвращает из JSON список словарей с финансовыми транзакциями'''
    my_list = []
    if not os.path.exists(path):
        raise FileNotFoundError("Файл не найден")
    if os.path.getsize(path) == 0:
        raise ValueError("Файл пустой")
    try:
        with open(path, encoding='utf-8') as finans_file:
            try:
                list_tr_actions = json.load(finans_file)
            except json.JSONDecodeError:
                print("Ошибка обработки кода")
                return my_list
    except FileNotFoundError:
        print("Файл не найден")
        return my_list
    return list_tr_actions


# if __name__ == '__main__':
#    list_j = get_finans_tranz("date\\oper1.json")
#    print(list_j)


def get_t_action_currency(tr_action: dict, amount=None) -> float:
    '''Функция принимает тразакцию и возвращет её сумму'''
#    amount_rub = ""
    if tr_action == {}:
        raise TypeError("Транзакция пустая")
    for i in tr_action:
        if 'operationAmount' not in i:
            raise KeyError("Ключ не найден")
        summ_amount = i["operationAmount"]["amount"]
        try:
            float(summ_amount)
        except ValueError:
            raise ValueError("Некорректная сумма")
        if float(summ_amount) <= 0.0:
            raise ValueError("Некорректная сумма")
        if i["operationAmount"]["currency"]["code"] == "RUB":
            amount_rub = float(i["operationAmount"]["amount"])
        elif i["operationAmount"]["currency"]["code"] == "USD" or "EUR":
            amount = i["operationAmount"]["amount"]
            currency = i["operationAmount"]["currency"]["code"]
            amount_rub = get_user_convert(amount, currency)
        else:
            continue
    return amount_rub


# list_j = get_finans_tranz("date\\oper1.json")
# amount_rub = get_t_action_currency(list_j)
# print(f"Сумма транзакции {amount_rub} руб.")
