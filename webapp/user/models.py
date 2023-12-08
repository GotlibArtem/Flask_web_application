from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db


class User(db.Model, UserMixin):
    """
    Описание таблицы БД зарегистрированных пользователей
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(512))
    role = db.Column(db.String(10), index=True)

    def set_password(self, password):
        """
        Функция хэширования пароля пользователя

        :param: пароль пользователя
        """
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """
        Функция проверки введенного пользователем пароля и
        зарегистриваронного в бд хэша пароля

        :param: пароль пользователя
        :return: результат проверки
        """
        return check_password_hash(self.password, password)

    @property
    def is_admin(self) -> bool:
        """
        Функция проверки роли пользователя на администратор

        :return: результат проверки
        """
        return self.role == 'admin'

    def __repr__(self) -> str:
        """
        Функция отображения в командной строке данных пользователя,
        который только что зашел в приложение

        :return: имя пользователя, который только что зашел
        """
        return f'User {self.email}, role {self.role}'
