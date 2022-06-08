# Librerias necesarias para el funcionamiento del codigo
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import autenticate, identity  # Libreria creada por nosotros
from Resources.user import UserRegister
from Resources.item import Item, ItemList
from Models.user import UserModel
from db import db
from Resources.store import Store, StoreList

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///data.db"  # le decimos que queremos que use la base de datos que se le proporciona dentro de la sentencia
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False  # le mecionamos a la extencion sqlachemy que no es necesario que rastree todos los datos que modificamos
app.secret_key = "jose"  # llave segura
api = Api(app)

jwt = JWT(app, autenticate, identity)  # nuevo autenticador /auth

# rutas de las que tomaremos los endpoints
# Rutas de items
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
# Ruta de registro de usuario
api.add_resource(UserRegister, "/register")
# Rutas de tiendas
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
