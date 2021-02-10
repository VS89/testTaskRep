from flask import Flask, request
from webService.testDB import func_db

app = Flask(__name__)

SUCCESS_STATUS_CODE = 200
ERROR_STATUS_CODE = 404
MAX_LEN_NAME_OR_SURNAME = 255


@app.route("/get_user_by_id")
def get():
    """
    Функция получения пользователя по ID
    :return: пользователя и код SUCCESS_STATUS_CODE если все ок, иначе error message и код ERROR_STATUS_CODE
    """
    id_user = request.args.get('id')
    if not id_user or not id_user.isdigit():
        return 'Вы ввели некорректные данные', ERROR_STATUS_CODE
    user = func_db.get_user_by_id(id_user)
    if user.json:
        return user, SUCCESS_STATUS_CODE
    return "Пользователь не найден", ERROR_STATUS_CODE


@app.route("/create_new_user")
def post():
    """
    Функция добавления пользователя в таблицу
    :return: id созданного пользователя и код SUCCESS_STATUS_CODE, иначе error message и код ERROR_STATUS_CODE
    """
    name = request.args.get('name')
    surname = request.args.get('surname')
    if not name and not surname:
        return 'Заполните поля имени и фамилии', ERROR_STATUS_CODE
    elif not name or len(name) > MAX_LEN_NAME_OR_SURNAME:
        return 'Вы ввели некорректное имя, оно пустое, либо содержит более 255 символов', ERROR_STATUS_CODE
    elif not surname or len(surname) > MAX_LEN_NAME_OR_SURNAME:
        return 'Вы ввели некорректную фамилию, она пустая, либо содержит более 255 символов', ERROR_STATUS_CODE
    user_id = func_db.insert_new_user(name, surname)
    if user_id:
        return user_id, SUCCESS_STATUS_CODE
    return 'Пользователь не создан', ERROR_STATUS_CODE


@app.route("/update_user")
def put():
    """
    Функция обновления данных у пользователя
    :return: отредактированного пользователя и код SUCCESS_STATUS_CODE, иначе error message и код ERROR_STATUS_CODE
    """
    id_user = request.args.get('id')
    name = request.args.get('name')
    surname = request.args.get('surname')
    if not id_user:
        return 'Для редактирования пользователя нужно обязательно указать ID', ERROR_STATUS_CODE
    elif not func_db.get_user_by_id(id_user).json:
        return 'Пользователя с таким ID не существует', ERROR_STATUS_CODE
    elif not name or not surname:
        return 'Поля имени или фамилии осталось пустым, должно быть заполнено', ERROR_STATUS_CODE
    elif len(name) > MAX_LEN_NAME_OR_SURNAME or len(surname) > MAX_LEN_NAME_OR_SURNAME:
        return f'Редактируемые данные должны быть < {MAX_LEN_NAME_OR_SURNAME} символов', ERROR_STATUS_CODE
    else:
        return func_db.update_user(id_user, name, surname), SUCCESS_STATUS_CODE


@app.route("/delete_user")
def delete():
    """
    Функция удаления пользователя
    :return: success message и код SUCCESS_STATUS_CODE, иначе error message и код ERROR_STATUS_CODE
    """
    id_user = request.args.get('id')
    if not id_user or not id_user.isdigit():
        return 'Вы ввели некорректные данные', ERROR_STATUS_CODE
    user = func_db.get_user_by_id(id_user)
    if not user.json:
        return f'Пользователь с ID: {id_user} уже удален', SUCCESS_STATUS_CODE
    user = func_db.delete_user_by_id(id_user)
    if user:
        return f"Пользователь с ID = {id_user} успешно удален", SUCCESS_STATUS_CODE
    return f"Пользователь с ID = {id_user} не был удален", ERROR_STATUS_CODE


if __name__ == "__main__":
    app.run(debug=True)
