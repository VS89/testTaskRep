import pytest
import allure
import requests
import random
import string
from tests.conftest import MAIN_URL, SUCCESS_STATUS_CODE, ERROR_STATUS_CODE, MAX_LEN_NAME_OR_SURNAME


@allure.feature('Добавление пользователя')
@pytest.mark.regression
@pytest.mark.create_user
class TestPostUser:
    """
    Класс, в котором собраны тесты, проверяющие добавление пользователя
    """

    URL_METHOD = f'{MAIN_URL}/create_new_user?name=%s&surname=%s'
    NAME = ''.join(random.choices(string.ascii_letters, k=15))
    SURNAME = ''.join(random.choices(string.ascii_letters, k=15))
    NAME_MORE_255 = ''.join(random.choices(string.ascii_letters, k=MAX_LEN_NAME_OR_SURNAME + 1))
    SURNAME_MORE_255 = ''.join(random.choices(string.ascii_letters, k=MAX_LEN_NAME_OR_SURNAME + 1))
    ERROR_MSG_NAME = 'Вы ввели некорректное имя, оно пустое, либо содержит более 255 символов'
    ERROR_MSG_SURNAME = 'Вы ввели некорректную фамилию, она пустая, либо содержит более 255 символов'
    ERROR_MSG_NAME_AND_SURNAME_EMPTY = 'Заполните поля имени и фамилии'

    @pytest.mark.parametrize('user', [{'name': '', 'surname': SURNAME},
                                      {'name': NAME, 'surname': ''},
                                      {'name': '', 'surname': ''}])
    @allure.title('Нельзя сохранить пользователя без имени или без фамилии')
    def test_not_save_user_without_name_or_surname(self, user):
        response = requests.get(self.URL_METHOD % (user['name'], user['surname']))
        if not user['name'] and not user['surname']:
            assert response.text == self.ERROR_MSG_NAME_AND_SURNAME_EMPTY, 'Неверный текст ошибки, если оба поля пустые'
        elif not user['name']:
            assert response.text == self.ERROR_MSG_NAME, 'Неверный текст ошибки для имени пользователя'
        elif not user['surname']:
            assert response.text == self.ERROR_MSG_SURNAME, 'Неверный текст ошибки для фамилии пользователя'
        assert response.status_code == ERROR_STATUS_CODE, \
            f'Неверный статус код, должен быть {ERROR_STATUS_CODE}'

    @pytest.mark.parametrize('user', [{'name': NAME_MORE_255, 'surname': SURNAME},
                                      {'name': NAME, 'surname': SURNAME_MORE_255}])
    @allure.title('Нельзя сохранить пользователя если его имя или фамиля >255 символов')
    def test_not_save_user_name_or_surname_which_has_more_255_char(self, user):
        response = requests.get(self.URL_METHOD % (user['name'], user['surname']))
        if len(user['name']) > MAX_LEN_NAME_OR_SURNAME:
            assert response.text == self.ERROR_MSG_NAME, 'Неверный текст ошибки для имени пользователя'
        elif len(user['surname']) > MAX_LEN_NAME_OR_SURNAME:
            assert response.text == self.ERROR_MSG_SURNAME, 'Неверный текст ошибки для фамилии пользователя'
        assert response.status_code == ERROR_STATUS_CODE, \
            f'Неверный статус код, должен быть {ERROR_STATUS_CODE}'

    @allure.title('Сохранение пользователя с корректными данными')
    def test_save_user_with_correct_data(self):
        response = requests.get(self.URL_METHOD % (self.NAME, self.SURNAME))
        assert response.text.isdigit(), 'Метод создания пользователя должен был вернуть число(ID)'
        assert response.status_code == SUCCESS_STATUS_CODE, f'Статус код должен быть {SUCCESS_STATUS_CODE}'
