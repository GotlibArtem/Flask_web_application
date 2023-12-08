from getpass import getpass
import sys

from webapp import create_app
from webapp.db import db
from webapp.user.models import User

app = create_app()

with app.app_context():
    user_email = input('Введите почту:')

    if User.query.filter(User.email == user_email).count():
        print('Пользователь с такой почтой уже зарегистрирован!')
        sys.exit(0)

    password1 = getpass('Введите пароль:')
    password2 = getpass('Повторите пароль:')

    if not password1 == password2:
        print('Пароли не совпадают!')
        sys.exit(0)

    new_user = User(email=user_email, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print(f'Создан пользователь с id = {new_user.id}')
