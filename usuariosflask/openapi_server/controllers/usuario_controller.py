import connexion
from typing import Dict
from typing import Tuple
from typing import Union


from openapi_server.models.usuario import Usuario  # noqa: E501
from openapi_server.models.usuario_update import UsuarioUpdate  # noqa: E501
from openapi_server import util

## Importa la app de Flask
from flask import app
from flask_sqlalchemy import SQLAlchemy

from openapi_server.models.perfil import Perfil



def actualizar_usuario(user_id, usuario_update):  # noqa: E501
    """Actualizar un usuario existente

    Actualiza la información de un usuario específico por su ID. # noqa: E501

    :param user_id: ID del usuario a actualizar
    :type user_id: int
    :param usuario_update: Objeto del usuario con la información actualizada
    :type usuario_update: dict | bytes

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        usuario_update = UsuarioUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def crear_usuario(usuario):  # noqa: E501
    """Crear un nuevo usuario

    Crea un nuevo usuario con la información proporcionada. # noqa: E501

    :param usuario: Objeto del usuario a crear
    :type usuario: dict | bytes

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        usuario = Usuario.from_dict(connexion.request.get_json())  # noqa: E501
        return 'do some magic!'



def eliminar_usuario(user_id):  # noqa: E501
    """Eliminar un usuario

    Elimina un usuario específico por su ID. # noqa: E501

    :param user_id: ID del usuario a eliminar
    :type user_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_usuarios():  # noqa: E501
    """Listar todos los usuarios

    Obtiene una lista de todos los usuarios disponibles en el sistema. # noqa: E501


    :rtype: Union[List[Usuario], Tuple[List[Usuario], int], Tuple[List[Usuario], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_usuario(user_id):  # noqa: E501
    """Obtener un usuario específico

    Obtiene la información detallada de un usuario específico por su ID. # noqa: E501

    :param user_id: ID del usuario a obtener
    :type user_id: int

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    return 'do some magic!'
