# Простое веб-приложение на Flask (flask_web_application)
Данный проект реализован для демонстрации своих навыков по тестовому заданию.
В рамках данного веб-приложения реализован следующий функционал:
* регистрация, аутентификация и авторизация пользователей;
* создание, просмотр, изменение и удаление заметок пользователя (для демонстрации выполнения CRUD операций);
* отображение погодных условий по городу, указанного пользователем (интеграция с внешним api). 

Для хранения данных используется база данных PostgreSQL.

## Установка и настройка проекта
1. Клонируйте репозиторий:
```
git clone https://github.com/GotlibArtem/flask_web_application.git
```
2. Создайте базу данных PostgreSQL через pgAdmin или иную СУБД.
3. В папке 'flask_web_application\webapp' создайте файл 'config.py' и опишите в нем переменные:
```
DB_NAME = 'Наименование вашей базы данных'

# Ваше путь/URI к базе данных
SQLALCHEMY_DATABASE_URI = f'postgresql://login:password@localhost:port/{DB_NAME}'
# Статус отслеживания измененных объектов и их вывода
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'Ваш секретный ключ для защиты от CSRF-атак'

# API ключ доступа к погодным условиям (https://weatherstack.com)
WEATHER_KEY = '236a15e449e790249595c79f1d5984a8'
```
4. Создайте и запустите виртуальное окружение:
```
python -m venv env
env\scripts\activate
```
5. Установите зависимости:
```
pip install -r requirements.txt
```
6. Выполните миграции для создания таблиц в БД:
```
set FLASK_APP=webapp
flask db init
flask db migrate -m "Создание таблиц user и note в БД"
flask db upgrade
```
7. Запустите файл, чтобы создать пользователя - администратор:
```
python create_admin.py
```
Заполните запрашиваемые данные в консоли.

## Запуск
Чтобы запустить веб-приложение, выполните в консоли:
```
run
```
