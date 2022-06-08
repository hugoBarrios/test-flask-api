from email import message
import sqlite3
from flask_restful import Resource, reqparse
from Models.user import UserModel

# clase para poder registrar nosotros mismos nuestros nuevos propios usuairios
class UserRegister(Resource):
    # Requerimos los datos que se le pasaran
    parser = reqparse.RequestParser()
    # Mencionamos que el campo del nombre de usuario no puede estar vacio
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be blank"
    )  # Mencionamos que el campo de contraseña tampoco debe estar vacio
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank"
    )

    def post(self):
        # Nos aseguramos nuevamente que los valores que se ingresaron esten cumpliendo las reglas
        data = UserRegister.parser.parse_args()
        # realizamos una busqueda para saber si este usuario existe o  no
        if UserModel.find_by_username(data["username"]):
            return {
                "message": "The user already exist"
            }, 400  # en caso si existiera estamos mencionando que es un error de peticion
        user = UserModel(**data)
        user.save_to_db()

        return {
            "message": "User Created Successfully"
        }, 201  # al finalizar el proceso mencionamos que el dato fue almacenado
