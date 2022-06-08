from db import db

# creamos el modelo de base de datos para la tabla de tienda
class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(
        db.Integer, primary_key=True
    )  # al usar INTEGER estamos colocando la propiedad de autoincremeneto
    name = db.Column(db.String(80))

    items = db.relationship(
        "ItemModel", lazy="dynamic"
    )  # Inicializamos una relacion recursiva

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            "name": self.name,
            "items": [item.json() for item in self.items.all()],
        }  # Esta es la mejor manera de retornar valores que se encuentren en relaciones

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # Tratamos de realizar los procesos de almacenado y eliminado de la base de datos dentro de nuestro programa
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
