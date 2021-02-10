import pytest
import random
import string
import requests

MAIN_URL = 'http://127.0.0.1:5000'
SUCCESS_STATUS_CODE = 200
ERROR_STATUS_CODE = 404
MAX_LEN_NAME_OR_SURNAME = 255


@pytest.fixture()
def create_user_id():
    """
    Фикстура которая создает клиента и удаляет его после завершения теста
    :return: id клиента
    """
    name = ''.join(random.choices(string.ascii_letters, k=15))
    surname = ''.join(random.choices(string.ascii_letters, k=15))
    user_id = requests.get(f'{MAIN_URL}/create_new_user?name={name}&surname={surname}')
    yield user_id.text
    requests.get(f'{MAIN_URL}/delete_user?id={user_id}')
