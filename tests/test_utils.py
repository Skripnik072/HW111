from unittest.mock import patch, mock_open

import pytest
from src.utils import get_finans_tranz, get_t_action_currency


@pytest.fixture
def path_json():
    '''Фикстура для задания абсолютного пути к файлу'''
    import os
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Поднимаемся на уровень выше (в корень)
    return os.path.join(base_dir, 'date', 'oper1.json')


@pytest.mark.parametrize("expected",
                         [([
                             {'id': 441945886,
                              'state': 'EXECUTED',
                              'date': '2019-08-26T10:50:58.294041',
                              'operationAmount':
                              {'amount': '31957.58',
                               'currency':
                               {'name': 'руб.',
                                'code': 'RUB'}
                               },
                              'description': 'Перевод организации',
                              'from': 'Maestro 1596837868705199',
                              'to': 'Счет 64686473678894779589'
                              },
                         ])])

def test_get_finans_tranz(path_json, expected):
    assert get_finans_tranz(path_json) == expected


@patch('builtins.open', new_callable=mock_open) # для отключения вызова файла
@patch('json.load')
@patch('os.path.exists', return_value=True) # добавили для отключения проверки наличия файла
@patch('os.path.getsize', return_value=1) # для отключения проверки размера файла
def test_get_json_load(mock_getsize, mock_exists, mock_json, mock_file):
    mock_json.return_value = ["test"]
    assert get_finans_tranz("test") == ["test"]
    mock_file.assert_called_once_with("test", encoding='utf-8')
    mock_json.assert_called_once()


def test_cod_error():
    with pytest.raises(FileNotFoundError, match="Файл не найден"):
        get_finans_tranz('oper1.json')


def test_file_empty(tmp_path):
    empty_file = tmp_path / "empty.json"
    empty_file.write_text("")
    with pytest.raises(ValueError, match="Файл пустой"):
        get_finans_tranz(str(empty_file))


@pytest.fixture
def tr_action():
    return [{'id': 441945886,'state': 'EXECUTED','date': '2019-08-26T10:50:58.294041'}]


def test_key_currency(tr_action):
    with pytest.raises(KeyError, match="Ключ не найден"):
        get_t_action_currency(tr_action, "1010")


@pytest.fixture
def tr_action_full():
    my_list = [
        {'id': 441945886,
         'state': 'EXECUTED',
         'date': '2019-08-26T10:50:58.294041',
         'operationAmount':
             {'amount': '31957.58',
              'currency':
                  {'name': 'руб.',
                   'code': 'RUB'}
              },
         'description': 'Перевод организации',
         'from': 'Maestro 1596837868705199',
         'to': 'Счет 64686473678894779589'
         },
    ]
    return my_list

def test_get_t_action_currency(tr_action_full: str) -> None:
    assert get_t_action_currency(tr_action_full) == 31957.58


@pytest.fixture
def tr_action_minus():
    my_list1 = [
        {'id': 441945886,
         'state': 'EXECUTED',
         'date': '2019-08-26T10:50:58.294041',
         'operationAmount':
             {'amount': '-31957.58',
              'currency':
                  {'name': 'руб.',
                   'code': 'RUB'}
              },
         'description': 'Перевод организации',
         'from': 'Maestro 1596837868705199',
         'to': 'Счет 64686473678894779589'
         },
    ]
    return my_list1


def test_value_currency_positiv(tr_action_minus: str) -> None:
    with pytest.raises(ValueError, match="Некорректная сумма"):
        get_t_action_currency(tr_action_minus, "0")


@pytest.fixture
def tr_action_text():
    my_list2 = [
        {'id': 441945886,
         'state': 'EXECUTED',
         'date': '2019-08-26T10:50:58.294041',
         'operationAmount':
             {'amount': 'g1957.58',
              'currency':
                  {'name': 'руб.',
                   'code': 'RUB'}
              },
         'description': 'Перевод организации',
         'from': 'Maestro 1596837868705199',
         'to': 'Счет 64686473678894779589'
         },
    ]
    return my_list2


def test_value_currency_text(tr_action_text: str) -> None:
    with pytest.raises(ValueError, match="Некорректная сумма"):
        get_t_action_currency(tr_action_text, "0")
