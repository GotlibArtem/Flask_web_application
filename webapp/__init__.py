from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate

from webapp.db import db
from webapp.user.models import User
from webapp.note.views import blueprint as note_blueprint
from webapp.user.views import blueprint as user_blueprint
from webapp.weather.views import blueprint as weather_blueprint


def create_app() -> Flask:
    """
    Функция создания веб-приложения на Flask

    :return: flask web-application
    """
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(note_blueprint)
    app.register_blueprint(weather_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def main_page():
        return render_template(
            'main.html'
        )

    return app


def main():
    """
    Функция запуска веб-приложения
    """
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()
