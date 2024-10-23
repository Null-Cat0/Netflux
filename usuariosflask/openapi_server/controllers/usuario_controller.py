import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from sqlalchemy.util import methods_equivalent


from openapi_server.models.usuario import Usuario  # noqa: E501
from openapi_server.models.usuario_update import UsuarioUpdate  # noqa: E501
from openapi_server import util
from openapi_server import db

# Importa la app de Flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

from openapi_server.models.perfil import Perfil
from openapi_server.models.usuario import Usuario
from openapi_server.models.usuario_db import UsuarioDB

from openapi_server import connex_app, app


@app.route('/actualizar_usuario/<user_id>', methods=['PUT'])
def actualizar_usuario(user_id):  # noqa: E501
    """Actualizar un usuario existente

    Actualiza la información de un usuario específico por su ID. # noqa: E501

    :param user_id: ID del usuario a actualizar
    :type user_id: int
    :param usuario_update: Objeto del usuario con la información actualizada
    :type usuario_update: dict | bytes

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    if request.is_json:
        usuario_update = UsuarioUpdate.from_dict(request.get_json())  # noqa: E501
    
    usuario = Usuario.query.filter_by(user_id=user_id).first()
    if usuario is None:
        return jsonify({"message": "El usuario no existe", "status": "error"}), 404

    usuario.nombre = usuario_update.nombre
    usuario.correo_electronico = usuario_update.correo_electronico
    usuario.password = usuario_update.password
    usuario.pais = usuario_update.pais
    usuario.plan_suscripcion = usuario_update.plan_suscripcion
    usuario.dispositivos = usuario_update.dispositivos

    db.session.commit()

    return jsonify({"message": "Usuario actualizado con éxito", "status": "success"}), 200


@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():  # noqa: E501
    """Crear un nuevo usuario

    Crea un nuevo usuario con la información proporcionada. # noqa: E501

    :param usuario: Objeto del usuario a crear
    :type usuario: dict | bytes

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """

   # Capturar los datos enviados en el JSON
    if request.is_json:
        usuario_nuevo = Usuario.from_dict(request.get_json())  # noqa: E501

    if (usuario_nuevo):
        nuevo_usuario = UsuarioDB(
            nombre=usuario_nuevo.nombre,
            correo_electronico=usuario_nuevo.correo_electronico,
            password='admin',
            pais=usuario_nuevo.pais,
            plan_suscripcion=usuario_nuevo.plan_suscripcion,
            dispositivos=usuario_nuevo.dispositivos
        )
        print(nuevo_usuario.nombre)
        print(nuevo_usuario.correo_electronico)
        print(nuevo_usuario.password)

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuario creado con éxito", "status": "success"}), 201

@app.route('/eliminar_usuario/<user_id>', methods=['DELETE'])
def eliminar_usuario(user_id):  # noqa: E501
    """Eliminar un usuario

    Elimina un usuario específico por su ID. # noqa: E501

    :param user_id: ID del usuario a eliminar
    :type user_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """

    usuario = Usuario.query.filter_by(user_id=user_id).first()

    if usuario is None:
        return jsonify({"message": "El usuario no existe", "status": "error"}), 404
    else:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado con éxito", "status": "success"}), 200
    

@app.route('/listar_usuarios', methods=['GET'])
def listar_usuarios():  # noqa: E501
    """Listar todos los usuarios

    Obtiene una lista de todos los usuarios disponibles en el sistema. # noqa: E501


    :rtype: Union[List[Usuario], Tuple[List[Usuario], int], Tuple[List[Usuario], int, Dict[str, str]]
    """
    
    usuarios = Usuario.query.all()
    return jsonify([usuario.serialize() for usuario in usuarios]), 200


@app.route('/usuario/<user_id>', methods=['GET'])
def obtener_usuario(user_id):  # noqa: E501
    """Obtener un usuario específico

    Obtiene la información detallada de un usuario específico por su ID. # noqa: E501

    :param user_id: ID del usuario a obtener
    :type user_id: int

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    
    usuario = UsuarioDB.query.filter_by(user_id=user_id).first()

    if usuario is None:
        return jsonify({"message": "El usuario no existe", "status": "error"}), 404
    else:
        return jsonify(usuario.serialize()), 200
