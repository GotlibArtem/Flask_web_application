from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from webapp.note.forms import AddNoteForm, ChangeNoteForm
from webapp.note.forms import DeleteNoteForm, SearchNoteForm
from webapp.note.models import Note
from webapp.db import db


blueprint = Blueprint('note', __name__, url_prefix='/notes')


@blueprint.route('/', methods=['GET'], defaults={"page": 1})
@blueprint.route('/<int:page>', methods=['GET'])
def user_notes(page):
    """
    Страница отображения созданных заметок текущего пользователя

    :param page: номер страницы
    """
    per_page = 10
    title = 'Мои заметки'
    delete_note_form = DeleteNoteForm()
    search_note_form = SearchNoteForm()
    note_info = Note.query. \
        filter(Note.id_user == current_user.id). \
        paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'note/notes.html',
        page_title=title,
        delete_note_form=delete_note_form,
        search_note_form=search_note_form,
        pagination=note_info
    )


@blueprint.route('/search/<string:search_note>/',
                 methods=['GET'], defaults={"page": 1})
@blueprint.route('/search/<string:search_note>/<int:page>',
                 methods=['GET'])
def search_notes(search_note, page):
    """
    Страница отображения найденных заметок по поиску

    :param search_note: значение для поиска в заметке
    :param page: номер страницы
    """
    per_page = 10
    title = "Мои заметки"
    delete_note_form = DeleteNoteForm()
    search_note_form = SearchNoteForm()
    note_info = Note.query. \
        filter(Note.id_user == current_user.id). \
        filter((Note.note_name.ilike(f'%{search_note}%')) |
               (Note.note_body.ilike(f'%{search_note}%'))). \
        paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'note/search_notes.html',
        page_title=title,
        delete_note_form=delete_note_form,
        search_note_form=search_note_form,
        pagination=note_info,
        search_note=search_note
    )


@blueprint.route('/process-search', methods=['POST'])
def process_search():
    """
    Процесс поиска заметок
    """
    search_note_form = SearchNoteForm()
    if search_note_form.validate_on_submit():
        search_note = str(search_note_form.search_note.data)
        if search_note != '':
            return redirect(url_for('note.search_notes',
                                    search_note=search_note,
                                    page=1))

    return redirect(url_for('note.user_notes'))


@blueprint.route('/add_note')
def add_note():
    """
    Страница добавления новой заметки
    """
    title = 'Создание новое заметки'
    add_note_form = AddNoteForm()

    return render_template(
        'note/new_note.html',
        page_title=title,
        add_note_form=add_note_form
    )


@blueprint.route('/process-create-note', methods=['POST'])
def process_create_note():
    """
    Процесс добавления новой заметки
    """
    add_note_form = AddNoteForm()
    if add_note_form.validate_on_submit():
        new_note = Note(
            id_user=current_user.id,
            note_name=add_note_form.note_name.data,
            note_body=add_note_form.note_body.data
        )
        db.session.add(new_note)
        db.session.commit()
        flash('Заметка добавлена!')

        return redirect(url_for('note.user_notes'))

    for field, errors in add_note_form.errors.items():
        for error in errors:
            flash(error)

    return redirect(url_for('note.add_note'))


@blueprint.route('/delete-note/<int:id_note>', methods=['POST'])
def delete_note(id_note):
    """
    Процесс удаления заметки

    :param id_note: id заметки, которую необходимо удалить
    """
    delete_note_form = DeleteNoteForm()
    if delete_note_form.validate_on_submit():
        note_data = Note.query.get(id_note)
        db.session.delete(note_data)
        db.session.commit()
        flash(f'Заметка "{note_data.note_name}" удалена!')
        return redirect(url_for('note.user_notes'))

    flash(f'Возникла ошибка при удалении заметки "{note_data.note_name}".')
    return redirect(url_for('note.user_notes'))


@blueprint.route('/change_note/<int:id_note>')
def change_note(id_note):
    """
    Страница изменения заметки
    """
    title = 'Изменение заметки'
    change_note_form = ChangeNoteForm()
    note_data = Note.query.get(id_note)

    return render_template(
        'note/change_note.html',
        note_data=note_data,
        page_title=title,
        change_note_form=change_note_form
    )


@blueprint.route('/process-change-note/<int:id_note>', methods=['POST'])
def process_change_note(id_note):
    """
    Процесс изменения заметки
    """
    change_note_form = ChangeNoteForm()
    if change_note_form.validate_on_submit():
        note_data = Note.query.get(id_note)
        note_data.note_name = change_note_form.note_name.data
        note_data.note_body = change_note_form.note_body.data
        db.session.commit()
        flash('Заметка изменена!')

        return redirect(url_for('note.user_notes'))

    for field, errors in change_note_form.errors.items():
        for error in errors:
            flash(error)

    return redirect(url_for('note.user_notes'))
