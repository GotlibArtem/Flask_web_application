from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField

from wtforms.validators import DataRequired


class AddNoteForm(FlaskForm):
    """
    Форма добавления новой заметки
    """
    note_name = StringField(
        'Наименование заметки',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg"}
    )
    note_body = StringField(
        'Описание заметки',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg body-note"}
    )
    submit = SubmitField(
        'Добавить заметку',
        render_kw={"class": "btn btn-lg create-note"}
    )


class DeleteNoteForm(FlaskForm):
    """
    Форма удаления заметки
    """
    delete_submit = SubmitField(
        'Удалить',
        render_kw={"class": "border-0 btn-transition btn btn-outline-danger delete"}
    )


class ChangeNoteForm(FlaskForm):
    """
    Форма изменения заметки
    """
    note_name = StringField(
        'Наименование заметки',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg"}
    )
    note_body = StringField(
        'Описание заметки',
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg body-note"}
    )
    change_submit = SubmitField(
        'Изменить заметку',
        render_kw={"class": "border-0 btn-transition btn btn-outline-success change"}
    )


class SearchNoteForm(FlaskForm):
    """
    Форма поиска заметки
    """
    search_note = StringField(
        'Наименование заметки',
        render_kw={"class": "form-control me-1",
                   "placeholder": "Наименование заметки"}
    )
    search_submit = SubmitField(
        'Поиск',
        render_kw={"class": "btn btn-primary"}
    )
