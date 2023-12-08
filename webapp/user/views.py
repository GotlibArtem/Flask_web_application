from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp.user.forms import ChangeUserInfo, LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.db import db


blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    """
    Страница авторизации пользователя
    """
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))

    title = 'Авторизация пользователя'
    login_form = LoginForm()

    return render_template(
        'user/login.html',
        page_title=title,
        form=login_form
    )


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    """
    Страницы аутентификации пользователя
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Авторизация выполнена!')

            return redirect(url_for('main_page'))

    flash('Неправильная почта или пароль!')

    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    """
    Страница для выхода пользователя
    """
    logout_user()

    return redirect(url_for('main_page'))


@blueprint.route('/registration')
def registration():
    """
    Страница регистрации нового пользователя
    """
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))

    title = 'Регистрация пользователя'
    registration_form = RegistrationForm()

    return render_template(
        'user/registration.html',
        page_title=title,
        form=registration_form
    )


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    """
    Страница проверки данных, введенных пользователем при регистрации
    на сайте, и возвращения ошибки, если пользователь уже зарегистрирован
    """
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        new_user = User(
            username=registration_form.username.data,
            email=registration_form.email.data,
            role='user'
        )
        new_user.set_password(registration_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')

        return redirect(url_for('user.login'))

    for field, errors in registration_form.errors.items():
        for error in errors:
            flash(error)

    return redirect(url_for('user.registration'))


@blueprint.route('/user_info/<int:id_user>')
def user_info(id_user):
    """
    Страница отображения данных пользователя

    :param id_user: id пользователя
    """
    user_data = User.query.get(id_user)
    title = 'Данные пользователя'
    changeuserinfo_form = ChangeUserInfo()

    return render_template(
        'user/user_info.html',
        user_data=user_data,
        page_title=title,
        form=changeuserinfo_form
    )


@blueprint.route('/process-change-user-info/<int:id_user>', methods=['POST'])
def process_change_user_info(id_user):
    """
    Страницы изменения данных пользователя
    """
    changeuserinfo_form = ChangeUserInfo()

    if changeuserinfo_form.validate_on_submit():
        user_data = User.query.get(id_user)
        user_data.username = ''
        flash('Данные пользователя изменены!')

    return redirect(url_for('user.user_info'))
