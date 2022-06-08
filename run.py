# creamos el archivo para poder crear un metodo de ejecucion
from app import app
from db import db

db.init_app(app)

# Le decimos a nuestra propia aplicacion que antes de realizar cualquier consulta realizara la creacion de la base de datos y colocara todo dentro de ella
@app.before_first_request
def create_tables():
    db.create_all()
