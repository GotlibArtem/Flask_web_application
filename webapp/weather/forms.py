from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class CheckWeatherForm(FlaskForm):
    """
    Форма проверки погодных условий в городе
    """
    city_name = StringField(
        'Наименование города',
        render_kw={"class": "form-control",
                   "placeholder": "Наименование города"}
    )
    check_submit = SubmitField(
        'Проверить!',
        render_kw={"class": "btn btn-primary check"}
    )
