import sqlite3
from db import db


class UserModel(
    db.Model
):  # Una clase espesifica para poder hacer uso de esta colocamos variables claves que necesitaremos de cada usario
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True) #Crea una id incrementable de manera automatica por lo que no se llama dentro de la app
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # buscamos dentro de la seccion denuestra base de datos el usuario con el nombre que se le pase a la funcion
    # metodos mas faciles de realizar busquedas dentro de la base de datos
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # como el anterior buscamos por medio de un dato y en este caso es por su ID
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
