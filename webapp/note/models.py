from webapp.db import db


class Note(db.Model):
    """
    Описание таблицы БД созданных заметок
    """
    id_note = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note_name = db.Column(db.String(256))
    note_body = db.Column(db.String(1024))
