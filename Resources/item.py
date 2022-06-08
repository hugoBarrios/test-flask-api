import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from Models.item import ItemModel


# Seccionamios el codigo colocando la creacion de items dentro de un nuevo archivo
# Se llaman emdiante las clases para esta manera ejecturarlo mejor
class Item(Resource):
    # Dentro del parcer solocamos la variacion y la voncersion e un numero natural a decimal asi de manera mas facil poder mencionar si el dato es cooorecto no
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This Fields cannot be left blank!"
    )

    parser.add_argument(
        "store_id", type=int, required=True, help="Every item needs a Store ID"
    )

    @jwt_required()  # Hacemos necesario el JWT para realizar una operacion
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    # podemos colocar el decorador aca para poder verificar la autenticidad del usuario
    @jwt_required()
    def post(
        self, name
    ):  # Creamos un nuevo objeto mediante un endpoint de manera que tambien corroboramos que si existe muestre error
        if ItemModel.find_by_name(name):
            return {
                "message": "An item with name '{}' already exists.".format(name)
            }, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        # Hacemos uso de try para poder ejecitar el codigo de almacenar en caso este no resulte bien es necesario para poder comprender
        # cual es el eror o en todo caso comprender el uso del mismo
        try:
            item.save_to_db()  # Almacena los datos
        except:
            return {
                "message": "An error occurred inserting the item."
            }, 500  # Eror interno dentro del servidor

        return (
            item.json(),
            201,
        )  # En caso resultar efectivo todo mostrara un codigo de creacion exitosa

    # podemos colocar el decorador aca para poder verificar la autenticidad del usuario
    @jwt_required()
    def delete(
        self, name
    ):  # Eliminamos el item creado de manera que le pasamos el nombre del item a eliminar
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted."}
        return {"message": "Item not found."}, 404

    @jwt_required()  # Hacemos necesario el JWT para realizar una operacion
    def put(
        self, name
    ):  # Re creamos el item pero de esta manera podemos actualizaro de igual manrea, cambiando algun o algunos campos dentro del mismo
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        # Creada una lista con los datos dentro de ella se procede a realizar una validacion
        # Validacion para comprobar que el item  existe
        if item is None:
            try:  # se realiza el try para evitar cualquier error que pueda provocarse
                item = ItemModel(
                    name, **data
                )  # En caso no existir realizara la sentencia dde insertar el dato
            except:
                return {
                    "message": "An error occurred inserting data"
                }, 500  # caso contrario nos mostrara un error de servidor
        else:  # Si el item realmente esta almacenado
            try:
                item.price = data[
                    "price"
                ]  # en caso si existir realizara el proceso para poder actualizar el item
            except:
                return {
                    "message": "An error occurred updating data"
                }, 500  # Caso contrario mostrara un mensaje de error de servidor

        item.save_to_db()
        return item.json()  # Regresamos el datos que se tenia por añadir/actualizar


# Clase para poder mostar todos los elementos que se encuentran dentro de la BD
class ItemList(Resource):
    @jwt_required()  # Hacemos necesario el JWT para realizar una operacion
    def get(self):  # reiteramos todos los nombres como una lista
        return {"items": [item.json() for item in ItemModel.query.all()]}
