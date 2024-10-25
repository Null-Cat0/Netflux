import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.perfil import Perfil  # noqa: E501
from openapi_server.models.perfil_update import PerfilUpdate  # noqa: E501
from openapi_server.models.serie import Serie  # noqa: E501
from openapi_server import util

from sqlalchemy.util import methods_equivalent
from openapi_server import db

# Importa la app de Flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

from openapi_server.models.perfil import Perfil
from openapi_server.models.usuario import Usuario

from openapi_server.models.dispositivo import Dispositivo

from openapi_server.models.usuario_db import UsuarioDB
from openapi_server.models.perfil_db import PerfilDB
from openapi_server.models.dispositivo_db import DispositivoDB
from openapi_server.models.dispositivos_usuario_db import DispositivosUsuarioDB

from openapi_server import connex_app, app


def actualizar_perfil_usuario(user_id, profile_id, perfil_update):  # noqa: E501
    """Actualiza el perfil especificado

    Actualiza el perfil especificado de un usuario # noqa: E501

    :param user_id: ID del usuario específicado
    :type user_id: int
    :param profile_id: ID del perfil a obtener
    :type profile_id: int
    :param perfil_update: Objeto del perfil con la información actualizada
    :type perfil_update: dict | bytes

    :rtype: Union[Perfil, Tuple[Perfil, int], Tuple[Perfil, int, Dict[str, str]]
    """
    if request.is_json:
        perfil_update = PerfilUpdate.from_dict(request.get_json())  # noqa: E501
    return 'do some magic!'


def borrar_perfil_usuario(user_id, profile_id):  # noqa: E501
    """Borra el perfil especificado

    Borra el perfil especificado de un usuario # noqa: E501

    :param user_id: ID del usuario específicado
    :type user_id: int
    :param profile_id: ID del perfil a obtener
    :type profile_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'

@app.route('/usuario/<user_id>/perfiles', methods=['POST'])
def crear_perfil(user_id):  # noqa: E501
    """Añade un nuevo perfil al usuario especificado

    Crea un nuevo perfil para el usuario # noqa: E501

    :param user_id: ID del usuario a eliminar
    :type user_id: int
    :param perfil: Objeto del perfil a crear
    :type perfil: dict | bytes

    :rtype: Union[Perfil, Tuple[Perfil, int], Tuple[Perfil, int, Dict[str, str]]
    """
    if request.is_json:
        print(request.get_json())
        perfil_api = Perfil.from_dict(request.get_json())  # noqa: E501

    if (perfil_api):
        perfil_db = PerfilDB(
            user_id=perfil_api.user_id,
            nombre=perfil_api.nombre,
        )
        db.session.add(perfil_db)
        db.session.commit()
        return jsonify(perfil_db.serialize()), 201
    return 'do some magic!'


def obtener_historial_perfil(user_id, profile_id):  # noqa: E501
    """Obtiene el historial de contenido completado por de un perfil

    Obtiene el historial de contenido completado por un perfil. Esta lista contendrá las series o películas terminadas de ver por el perfil. # noqa: E501

    :param user_id: ID del usuario específicado
    :type user_id: int
    :param profile_id: ID del perfil específico
    :type profile_id: int

    :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_lista_perfil(user_id, profile_id):  # noqa: E501
    """Obtiene la lista de un perfil concreto

    Obtiene la lista de contenidos guardados para ver de un perfil # noqa: E501

    :param user_id: ID del usuario específicado
    :type user_id: int
    :param profile_id: ID del perfil específico
    :type profile_id: int

    :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_perfil_usuario(user_id, profile_id):  # noqa: E501
    """Obtiene el perfil específico de un usuario concreto

    Obtiene el perfil específico de un usuario concreto # noqa: E501

    :param user_id: ID del usuario específicado
    :type user_id: int
    :param profile_id: ID del perfil a obtener
    :type profile_id: int

    :rtype: Union[Perfil, Tuple[Perfil, int], Tuple[Perfil, int, Dict[str, str]]
    """
    return 'do some magic!'

@app.route('/usuario/<user_id>/perfiles', methods=['GET'])
def obtener_perfiles(user_id):  # noqa: E501
    """Obtiene todos los perfiles del usuario especificado

    Lista los perfiles de un usuario # noqa: E501

    :param user_id: ID del usuario a eliminar
    :type user_id: int

    :rtype: Union[List[Perfil], Tuple[List[Perfil], int], Tuple[List[Perfil], int, Dict[str, str]]
    """
    
    perfiles = PerfilDB.query.filter_by(user_id=user_id).all()
    
    if perfiles is None:
        return jsonify({"message": "No hay perfiles disponibles", "status": "error"}), 404
    else:
        return jsonify([perfil.serialize() for perfil in perfiles]), 200    
    
    return 'do some magic!'
