from flask_restful import Resource
from Models.store import StoreModel

#creamos el prinripio de "tienda" para ser usado 
class Store(Resource):
    def get(self, name): #obtenemos las tiendas que estan creadas por nombre
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    def post(self, name): #Creamos y almacenamos una tienda nueva si no esta creada
        if StoreModel.find_by_name(name):
            return {
                "message": "A store with name '{}' already exists.".format(name)
            }, 400

        store = StoreModel(name) #le decimos que el modelo de tienda se le esta pasando el nombre de la tienda
        try:
            store.save_to_db() #es almacenada en la base de datos
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    def delete(self, name): #en caso es necesrio borramos las tiendas por nombre
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Store deleted"}

#obtenemos todas las tiendas que se encuentren en la base de datos
class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
