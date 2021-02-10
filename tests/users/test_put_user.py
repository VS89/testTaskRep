import pytest
import allure
import requests
import random
import string
from tests.conftest import MAIN_URL, SUCCESS_STATUS_CODE, ERROR_STATUS_CODE, MAX_LEN_NAME_OR_SURNAME


@allure.feature('Обновление данных пользователя')
@pytest.mark.regression
@pytest.mark.update_user
class TestPutUser:
    """
    Класс, в котором собраны тесты, проверяеющие работу обновления данных пользователя
    """

    URL_METHOD = f'{MAIN_URL}/update_user?id=%s&name=%s&surname=%s'
    DATA_TYPE = 'application/json'
    ID_USER = '5'
    NOT_USER_ID = '2'
    NAME = ''.join(random.choices(string.ascii_letters, k=15))
    SURNAME = ''.join(random.choices(string.ascii_letters, k=15))
    NAME_MORE_255 = ''.join(random.choices(string.ascii_letters, k=MAX_LEN_NAME_OR_SURNAME + 1))
    SURNAME_MORE_255 = ''.join(random.choices(string.ascii_letters, k=MAX_LEN_NAME_OR_SURNAME + 1))
    ERROR_EMPTY_ID_USER = 'Для редактирования пользователя нужно обязательно указать ID'
    ERROR_ID_USER = 'Пользователя с таким ID не существует'
    ERROR_EMPTY_NAME_OR_SURNAME = 'Поля имени или фамилии осталось пустым, должно быть заполнено'
    ERROR_MAX_LEN_CHAR = f'Редактируемые данные должны быть < {MAX_LEN_NAME_OR_SURNAME} символов'

    @allure.title('Редактирование пользователя')
    def test_update_user_have_id_and_correct_data(self):
        response = requests.get(self.URL_METHOD % (self.ID_USER, self.NAME, self.SURNAME))
        assert response.status_code == SUCCESS_STATUS_CODE, f'Статус код должен быть {SUCCESS_STATUS_CODE}'
        assert response.headers['Content-Type'] == self.DATA_TYPE, f'тип данных должен быть {self.DATA_TYPE}'
        user_json = response.json()
        assert user_json[0]['name'] == self.NAME, f'Имя пользователя не было отредактировано'
        assert user_json[0]['surname'] == self.SURNAME, f'Фамилия пользователя не была отредактирована'

    @allure.title('Нельзя редактировать пользователя, если не передали ID')
    def test_update_user_empty_id(self):
        response = requests.get(self.URL_METHOD % ('', self.NAME, self.SURNAME))
        assert response.status_code == ERROR_STATUS_CODE, f'Статус код должен быть {ERROR_STATUS_CODE}'
        assert response.text == self.ERROR_EMPTY_ID_USER, f'Неверный текст ошибки'

    @allure.title('Нельзя отредактировать пользователя с ID которого нет')
    def test_update_user_not_user_id(self):
        response = requests.get(self.URL_METHOD % (self.NOT_USER_ID, self.NAME, self.SURNAME))
        assert response.status_code == ERROR_STATUS_CODE, f'Статус код должен быть {ERROR_STATUS_CODE}'
        assert response.text == self.ERROR_ID_USER, f'Неверный текст ошибки'

    @pytest.mark.parametrize('user', [{'name': '', 'surname': SURNAME}, {'name': NAME, 'surname': ''}])
    @allure.title('Нельзя отредактировать пользователя, если передать ему пустое имя или фамилию')
    def test_update_user_empty_name_or_surname(self, user):
        response = requests.get(self.URL_METHOD % (self.ID_USER, user['name'], user['surname']))
        assert response.status_code == ERROR_STATUS_CODE, f'Статус код должен быть {ERROR_STATUS_CODE}'
        assert response.text == self.ERROR_EMPTY_NAME_OR_SURNAME, f'Неверный текст ошибки'

    @pytest.mark.parametrize('user', [{'name': NAME_MORE_255, 'surname': SURNAME},
                                      {'name': NAME, 'surname': SURNAME_MORE_255}])
    @allure.title('Нельзя отредактировать пользователя если его имя или фамилия содержит > 255 символов')
    def test_update_user_more_max_len_name_or_surname(self, user):
        response = requests.get(self.URL_METHOD % (self.ID_USER, user['name'], user['surname']))
        assert response.status_code == ERROR_STATUS_CODE, f'Статус код должен быть {ERROR_STATUS_CODE}'
        assert response.text == self.ERROR_MAX_LEN_CHAR, f'Неверный текст ошибки'
