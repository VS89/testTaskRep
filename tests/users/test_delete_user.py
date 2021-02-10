import pytest
import allure
import requests
from tests.conftest import MAIN_URL, SUCCESS_STATUS_CODE, ERROR_STATUS_CODE


@allure.feature('Удаление пользователя по ID')
@pytest.mark.regression
@pytest.mark.delete_user
class TestDeleteUser:
    """
    Класс, в котором собраны тесты, проверяеющие работу функции удаления пользователя по ID
    """

    URL_METHOD_WITH_PARAM = f'{MAIN_URL}/delete_user?id='
    URL_METHOD_GET_USER = f'{MAIN_URL}/get_user_by_id?id='
    NOT_USER_ID = '2'
    INVALID_ID = 'asdqweq'
    EMPTY_ID = ''
    ERROR_INCORRECT_DATA = 'Вы ввели некорректные данные'
    ERROR_USER_NOT_FOUND = 'Пользователь не найден'
    SUCCESS_DELETE = 'Пользователь с ID = %s успешно удален'
    USER_ALREADY_DELETE = 'Пользователь с ID: %s уже удален'

    @allure.title('Удаление пользователя который есть в базе данных')
    def test_delete_user_by_valid_id(self, create_user_id):
        with allure.step(f'удаляем пользователя с id: {create_user_id}'):
            response = requests.get(f'{self.URL_METHOD_WITH_PARAM}{create_user_id}')
            assert response.status_code == SUCCESS_STATUS_CODE, \
                f'статус код не {SUCCESS_STATUS_CODE}, клиент не был удален'
            assert response.text == self.SUCCESS_DELETE % create_user_id, \
                'неверное сообщение об успешном удалении клиента'

        with allure.step(f'проверим что пользователя с id: {create_user_id} действительно нет в базе'):
            response = requests.get(f'{self.URL_METHOD_GET_USER}{create_user_id}')
            assert response.status_code == ERROR_STATUS_CODE, f'статус код не {ERROR_STATUS_CODE}'
            assert response.text == self.ERROR_USER_NOT_FOUND

    @allure.title('Удаление пользователя с некорректным ID')
    @pytest.mark.parametrize('user_id', [INVALID_ID, EMPTY_ID])
    def test_delete_user_by_invalid_id(self, user_id):
        response = requests.get(f'{self.URL_METHOD_WITH_PARAM}{user_id}')
        assert response.status_code == ERROR_STATUS_CODE, f'статус код не {ERROR_STATUS_CODE}'
        assert response.text == self.ERROR_INCORRECT_DATA

    @allure.title('Удаление уже удаленного пользователя')
    def test_delete_user_not_user_id(self):
        response = requests.get(f'{self.URL_METHOD_WITH_PARAM}{self.NOT_USER_ID}')
        assert response.status_code == SUCCESS_STATUS_CODE, f'статус код не {SUCCESS_STATUS_CODE}'
        assert response.text == self.USER_ALREADY_DELETE % self.NOT_USER_ID
