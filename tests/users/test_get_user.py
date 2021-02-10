import pytest
import allure
import requests
from tests.conftest import MAIN_URL, SUCCESS_STATUS_CODE, ERROR_STATUS_CODE


@allure.feature('Получение пользователя по ID')
@pytest.mark.regression
@pytest.mark.get_user
class TestGetUser:
    """
    Класс, в котором собраны тесты, проверяеющие работу полечения пользователя по ID
    """

    VALID_ID = '9'
    NOT_USER_ID = '2'
    INVALID_ID = 'asdqwe'
    EMPTY_ID = ''
    URL_METHOD_WITH_PARAM = f'{MAIN_URL}/get_user_by_id?id='
    USER_NAME = 'hhlkj'
    USER_SURNAME = 'uiouioui'
    ERROR_USER_NOT_FOUND = 'Пользователь не найден'
    ERROR_INCORRECT_DATA = 'Вы ввели некорректные данные'
    DATA_TYPE = 'application/json'

    @allure.title('Пользователь есть в таблице, статус код = 200')
    def test_get_user_by_id_equals_status_code_200(self):
        with allure.step(f'для пользователя с id = {self.VALID_ID} статус код должен быть равен {SUCCESS_STATUS_CODE}'):
            response = requests.get(f'{self.URL_METHOD_WITH_PARAM}{self.VALID_ID}')
        with allure.step(f'проверим, что статус код равен {SUCCESS_STATUS_CODE}'):
            assert response.status_code == SUCCESS_STATUS_CODE, f'статус код не {SUCCESS_STATUS_CODE}'

    @allure.title('Данные пользователя приходят в формате JSON')
    def test_get_user_by_id_content_type_equals_json(self):
        response = requests.get(f'{self.URL_METHOD_WITH_PARAM}{self.VALID_ID}')
        assert response.headers['Content-Type'] == self.DATA_TYPE, f'тип данных должен быть {self.DATA_TYPE}'

    @allure.title('Верно передаются имя и фамилия пользователя')
    def test_get_user_by_id_check_name_and_surname(self):
        response = requests.get(f'{self.URL_METHOD_WITH_PARAM}{self.VALID_ID}')
        user_json = response.json()
        assert user_json[0]['name'] == self.USER_NAME, f'у пользователя с id = {self.VALID_ID} другое имя'
        assert user_json[0]['surname'] == self.USER_SURNAME, f'у пользователя с id = {self.VALID_ID} другая фамилия'

    @allure.title('Если пользователя с таким ID нет, то получаем пустой JSON и ошибку 404')
    def test_get_user_by_not_user_id(self):
        response = requests.get(f'{self.URL_METHOD_WITH_PARAM}{self.NOT_USER_ID}')
        assert response.status_code == ERROR_STATUS_CODE, f'статус код не {ERROR_STATUS_CODE}'
        assert response.text == self.ERROR_USER_NOT_FOUND

    @pytest.mark.parametrize('user_id', [INVALID_ID, EMPTY_ID])
    @allure.title('Если пользователя с таким ID нет, то получаем пустой JSON')
    def test_get_user_by_invalid_id(self, user_id):
        response = requests.get(f'{self.URL_METHOD_WITH_PARAM}{user_id}')
        assert response.status_code == ERROR_STATUS_CODE, f'статус код не {ERROR_STATUS_CODE}'
        assert response.text == self.ERROR_INCORRECT_DATA
