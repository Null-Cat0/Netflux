from openapi_server.models.usuario import Usuario  # noqa: E501
from openapi_server.models.usuario_update import UsuarioUpdate  # noqa: E501
from openapi_server import db

# Importa la app de Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy

from openapi_server.models.perfil import Perfil
from openapi_server.models.usuario import Usuario

from openapi_server.models.dispositivo import Dispositivo

from openapi_server.models.usuario_db import UsuarioDB
from openapi_server.models.perfil_db import PerfilDB
from openapi_server.models.dispositivo_db import DispositivoDB
from openapi_server.models.dispositivos_usuario_db import DispositivosUsuarioDB

from openapi_server import app


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
        usuario_update = UsuarioUpdate.from_dict(request.get_json())
    
    usuario = UsuarioDB.query.filter_by(user_id=user_id).first()
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
        usuario_api = Usuario.from_dict(request.get_json())  # noqa: E501

    if (usuario_api):
        usuario_db = usuario_api.to_db_model()

        existe_dispositivo = DispositivoDB.query.filter_by(nombre=usuario_api.dispositivos[0]).first()
        if existe_dispositivo is None:
            return jsonify({"message": "Ha habido un error con su solicitud, inténtelo de nuevo más tarde", "status": "error"}), 404

        db.session.add(usuario_db)
        db.session.commit()

        for dispositivo_nombre in usuario_api.dispositivos:
            disp_enc = DispositivoDB.query.filter_by(nombre=dispositivo_nombre).first()
            if disp_enc is not None:
                dispositivos_usuario_db = DispositivosUsuarioDB(
                    dispositivo_id=disp_enc.dispositivo_id,
                    user_id=usuario_db.user_id,
                )
                db.session.add(dispositivos_usuario_db)

        # Añadimos un perfil por defecto al usuario
        perfiles_db = PerfilDB(nombre=usuario_db.nombre, user_id=usuario_db.user_id)
        print(f"Datos del perfil_db:{perfiles_db.nombre}, {perfiles_db.user_id}")

        db.session.add(perfiles_db)
        # db.session.update(usuario_db)
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

    usuario = UsuarioDB.query.filter_by(user_id=user_id).first()


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
    
    list_usuarios_db = UsuarioDB.query.all()
    list_usuarios_api = [usuario.to_api_model() for usuario in list_usuarios_db]
    return jsonify([usuario.serialize() for usuario in list_usuarios_api]), 200


@app.route('/usuario/<user_id>', methods=['GET'])
def obtener_usuario(user_id):  # noqa: E501
    """Obtener un usuario específico

    Obtiene la información detallada de un usuario específico por su ID. # noqa: E501

    :param user_id: ID del usuario a obtener
    :type user_id: int

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    
    usuario_db = UsuarioDB.query.filter_by(user_id=user_id).first()
    # Hacer
    dispositivos_usuario_db = DispositivosUsuarioDB.query.filter_by(user_id=user_id).all()

    dispositivos = []
    for dispositivo_usuario_db in dispositivos_usuario_db:
        dispositivo = DispositivoDB.query.filter_by(dispositivo_id=dispositivo_usuario_db.dispositivo_id).first()
        if dispositivo:  # Solo agrega si el dispositivo existe
            dispositivos.append(dispositivo.nombre)

    print(dispositivos)  # Verificamos que la lista de dispositivos sea correcta

    if usuario_db is None:
        return jsonify({"message": "El usuario no existe", "status": "error"}), 405

    usuario_api = usuario_db.to_api_model()

    return jsonify(usuario_api.serialize()), 200
