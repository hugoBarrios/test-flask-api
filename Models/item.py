from operator import itemgetter
import sqlite3
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod  # Metodo para poder buscar productos por el nombre
    def find_by_name(cls, name):
        return cls.query.filter_by(
            name=name
        ).first()  # Opcion mas sencilla para hacer SELECT * FROM items WHERE name = name

    # .first nos devuelve el primer valor encontrado tras realizar la consuita a la base de datos
    # Metodo para pdoer insertar todos los datos de manera mas sencillla y facil.
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Sentencias mas simples y sencillas para realizar una insersion y eliminacion de datos dentro de la BD
    # Metodo empleado para poder realizar la actualizacion de valores dentro de la BD
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
