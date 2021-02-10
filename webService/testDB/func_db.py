import sqlite3
import json
from flask import jsonify

PATH_DB = 'testDB/user_db'


def insert_new_user(name: str, surname: str) -> str:
    """
    Функция, которая добавляет нового пользователя в таблицу user_db
    :param name: имя пользователя
    :param surname: фамилия пользователя
    :return: id добавленного пользователя
    """
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    with connection:
        cursor.execute('INSERT INTO user_db(name,surname) VALUES (:name,:surname)', {'name': name,
                                                                                     'surname': surname})
        cursor.execute('select * from user_db where name=:name', {'name': name})
        return str(cursor.lastrowid)


def get_user_by_id(id_user) -> json:
    """
    Функция получения пользователя по ID
    :param id_user: ID пользователя
    :return: json с данными о пользователе
    """
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    with connection:
        cursor.execute('select name, surname from user_db where id=:id', {'id': id_user})
        result = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    return jsonify(result)


def update_user(id_user: int, name: str, surname: str):
    """
    Функция для обновления имени и фамилии пользователя
    :param id_user: id пользователя
    :param name: имя
    :param surname: фамилия
    :return: измененного пользователя
    """
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    with connection:
        cursor.execute('UPDATE user_db SET name = :name, surname = :surname WHERE id = :id_user',
                       {'name': name, 'surname': surname, 'id_user': id_user})
    return get_user_by_id(id_user)


def delete_user_by_id(id_user: int):
    """
    Функция для удаления пользователя из таблицы
    :param id_user: id пользователя
    :return: True если пользователь был удален
    """
    connection = sqlite3.connect(PATH_DB)
    cursor = connection.cursor()
    with connection:
        cursor.execute('DELETE FROM user_db WHERE id = :id_user', {'id_user': id_user})
    return True
