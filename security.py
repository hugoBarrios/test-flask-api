from werkzeug.security import safe_str_cmp
from Models.user import UserModel


def autenticate(
    username, password
):  # Funcion para autenticar que el usuario realmente se encuentra en nuestro sistema
    user = UserModel.find_by_username(
        username
    )  # En caso no existe sera enfiado como defult None
    # El uso de safe_str_com compara de manea segura los datos que tenemos dentro del arreglo
    if user and safe_str_cmp(user.password, password):
        return user


def identity(
    payload,
):  # encontramos el token proporcionado por JWT para conocer el usuario que se encuentra
    user_id = payload["identity"]
    return UserModel.find_by_id(
        user_id
    )  # Esta busqueda sera retornado el ID del usuario y caso contrario None
