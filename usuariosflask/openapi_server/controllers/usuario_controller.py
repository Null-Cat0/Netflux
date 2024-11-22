# Se importa el fichero de configuración de los microservicios
import os, sys, requests
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(app_path)

from global_config import ContenidosConfig, UsuariosConfig

from werkzeug.security import generate_password_hash, check_password_hash

from openapi_server import app, db
from flask import request, jsonify

from openapi_server.models.usuario import Usuario
from openapi_server.models.usuario_db import UsuarioDB
from openapi_server.models.usuario_update import UsuarioUpdate  # noqa: E501

from openapi_server.models.perfil_db import PerfilDB
from openapi_server.models.dispositivo_db import DispositivoDB
from openapi_server.models.dispositivos_usuario_db import DispositivosUsuarioDB

@app.route('/actualizar_usuario/<int:user_id>', methods=['PUT'])
def actualizar_usuario(user_id):  # noqa: E501
    """Actualizar un usuario existente"""

    if request.is_json:
        usuario_update = UsuarioUpdate.from_dict(request.get_json())
        print(f"Valor de esAdmin en usuario_update: {usuario_update.esAdmin}")
    else:
        return jsonify({"message": "Solicitud no contiene JSON válido", "status": "error"}), 400

    # Buscar el usuario en la base de datos
    usuario = UsuarioDB.query.filter_by(user_id=user_id).first()
    if usuario is None:
        return jsonify({"message": "El usuario no existe", "status": "error"}), 404

    # Mostrar datos recibidos para verificación de debug
    print("Datos recibidos:", request.get_json())

    # Actualizar atributos del usuario
    usuario.nombre = usuario_update.nombre
    usuario.correo_electronico = usuario_update.correo_electronico
    usuario.pais = usuario_update.pais
    usuario.plan_suscripcion = usuario_update.plan_suscripcion

    # Convertir 'admin' a booleano correctamente
    usuario.esAdmin =  usuario_update.esAdmin
    print(f"Valor de esAdmin después de la conversión: {usuario.esAdmin}")

    # Eliminar los dispositivos actuales del usuario para agregar los nuevos
    DispositivosUsuarioDB.query.filter_by(user_id=user_id).delete()

    # Agregar nuevos dispositivos asociados al usuario
    for nombre in usuario_update.dispositivos:
        disp_enc = DispositivoDB.query.filter_by(tipo_dispositivo=nombre).first()
        if disp_enc:
            dispositivo_usuario_db = DispositivosUsuarioDB(
                dispositivo_id=disp_enc.dispositivo_id,
                user_id=usuario.user_id,
                nombre_dispositivo=f"{disp_enc.tipo_dispositivo} de {usuario.nombre}"
            )
            db.session.add(dispositivo_usuario_db)

    # Confirmar los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Usuario actualizado con éxito", "status": "success"}), 200



@app.route('/actualizar_password/<user_id>', methods=['PATCH'])
def actualizar_password(user_id):  # noqa: E501
    """Actualizar la contraseña de un usuario

    Actualiza la contraseña de un usuario específico por su ID después de verificar la contraseña antigua. # noqa: E501

    :param user_id: ID del usuario a actualizar
    :type user_id: int

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    
    # Verificar si los datos están en formato JSON
    if not request.is_json:
        return jsonify({"message": "La solicitud debe estar en formato JSON", "status": "error"}), 400

    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    # Verificar que ambas contraseñas se hayan proporcionado
    if not old_password or not new_password:
        return jsonify({"message": "Se requiere la contraseña actual y la nueva contraseña", "status": "error"}), 400

    # Buscar el usuario en la base de datos
    usuario = UsuarioDB.query.filter_by(user_id=user_id).first()
    if usuario is None:
        return jsonify({"message": "El usuario no existe", "status": "error"}), 404

    # Verificar que la contraseña antigua es correcta
    if not check_password_hash(usuario.password, old_password):
        return jsonify({"message": "La contraseña actual es incorrecta", "status": "error"}), 401

    # Actualizar la contraseña con el hash de la nueva contraseña
    usuario.password = generate_password_hash(new_password)
    db.session.commit()
    
    return jsonify({"message": "Contraseña actualizada con éxito", "status": "success"}), 200


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
        usuario_api.password = generate_password_hash(usuario_api.password)

    if (usuario_api):
        usuario_db = usuario_api.to_db_model()
        
        db.session.add(usuario_db)
        db.session.commit()

        for nombre in usuario_api.dispositivos:
            disp_enc = DispositivoDB.query.filter_by(tipo_dispositivo=nombre).first()
            if disp_enc is not None:
                dispositivos_usuario_db = DispositivosUsuarioDB(
                    dispositivo_id=disp_enc.dispositivo_id,
                    user_id=usuario_db.user_id,
                    nombre_dispositivo=disp_enc.tipo_dispositivo + " de " + usuario_db.nombre
                )
                db.session.add(dispositivos_usuario_db)

        # Se crear un perfil por defecto para el usuario
        payload = {
            "user_id": usuario_db.user_id,
            "nombre": usuario_db.nombre,
            "foto_perfil": 'netflux_rojo.png',
            "preferencias_contenido": {},
        }
        request_perfil = requests.post(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuario/{usuario_db.user_id}/perfiles", json=payload)

        if request_perfil.status_code != 201:
            return jsonify({"message": "Error al crear el perfil por defecto del usuario"}), 500

        # db.session.add(perfiles_db)
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
        request_borrar_perfiles = requests.delete(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuario/{user_id}/perfiles")

        if request_borrar_perfiles.status_code != 200:
            return jsonify({"message": "Error al borrar los perfiles del usuario"}), 500

        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado con éxito", "status": "success"}), 200
    
# @app.route('/listar_usuarios', methods=['GET'])
# def listar_usuarios():  # noqa: E501
#     """Listar todos los usuarios

#     Obtiene una lista de todos los usuarios disponibles en el sistema. # noqa: E501


#     :rtype: Union[List[Usuario], Tuple[List[Usuario], int], Tuple[List[Usuario], int, Dict[str, str]]
#     """
#     list_usuarios_db = UsuarioDB.query.all()
#     list_usuarios_api = [usuario.to_api_model() for usuario in list_usuarios_db]
#     return jsonify([usuario.serialize() for usuario in list_usuarios_api]), 200

@app.route('/usuario/<user_id>', methods=['GET'])
def obtener_usuario(user_id):  # noqa: E501
    """Obtener un usuario específico

    Obtiene la información detallada de un usuario específico por su ID. # noqa: E501

    :param user_id: ID del usuario a obtener
    :type user_id: int

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    usuario_db = UsuarioDB.query.filter_by(user_id=user_id).first()
    if usuario_db is None:
        return jsonify({"message": "El usuario no existe", "status": "error"}), 404
    else:
        dispositivos_usuario_db = DispositivosUsuarioDB.query.filter_by(user_id=user_id).all()
        dispositivos = []
        for dispositivo_usuario_db in dispositivos_usuario_db:
            dispositivo = DispositivoDB.query.filter_by(dispositivo_id=dispositivo_usuario_db.dispositivo_id).first()
            if dispositivo:  # Solo agrega si el dispositivo existe
                dispositivos.append(dispositivo.tipo_dispositivo)

    print(dispositivos)  # Verificamos que la lista de dispositivos sea correcta

    if usuario_db is None:
        return jsonify({"message": "El usuario no existe", "status": "error"}), 405

    usuario_api = usuario_db.to_api_model()

    return jsonify(usuario_api.serialize()), 200