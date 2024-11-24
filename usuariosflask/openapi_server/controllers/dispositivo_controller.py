from openapi_server.models.dispositivo_db import DispositivoDB
from openapi_server.models.dispositivos_usuario_db import DispositivosUsuarioDB

from openapi_server import app, db
from flask import request, jsonify

from openapi_server.models.actualizar_dispositivos_request import ActualizarDispositivosRequest

@app.route('/usuarios/<user_id>/dispositivos/<dispositivo_id>/<nombre_dispositivo>/', methods=['PUT'])
def actualizar_dispositivo(user_id, nombre_dispositivo, dispositivo_id):
    if request.is_json:
        actualizar_dispositivos_request = ActualizarDispositivosRequest.from_dict(request.get_json())

        dispositivo_usuario_db = DispositivosUsuarioDB.query.filter_by(
            user_id=user_id, dispositivo_id=dispositivo_id, nombre_dispositivo=nombre_dispositivo
        ).first()

        if dispositivo_usuario_db is not None:
            # Verificar si la nueva combinación ya existe para otro registro
            nuevo_nombre_dispositivo = actualizar_dispositivos_request.nombre_dispositivo
            nuevo_dispositivo_id = actualizar_dispositivos_request.dispositivo_id

            dispositivo_existente = DispositivosUsuarioDB.query.filter_by(
                user_id=user_id,
                nombre_dispositivo=nuevo_nombre_dispositivo,
                dispositivo_id=nuevo_dispositivo_id
            ).first()

            if dispositivo_existente and dispositivo_existente != dispositivo_usuario_db:
                return jsonify({"message": "Ya existe un dispositivo con los mismos datos", "status": "error"}), 400

            # Si no existe duplicado, proceder con la actualización
            if nuevo_nombre_dispositivo and nuevo_dispositivo_id:
                dispositivo_usuario_db.nombre_dispositivo = nuevo_nombre_dispositivo
                dispositivo_usuario_db.dispositivo_id = nuevo_dispositivo_id
                db.session.commit()
                return jsonify({"message": "Dispositivo actualizado con éxito", "status": "success"}), 200
            else:
                return jsonify({"message": "Datos incompletos para actualizar", "status": "error"}), 400
        else:
            return jsonify({"message": "El dispositivo no existe", "status": "error"}), 404

@app.route('/usuarios/<user_id>/dispositivos/<dispositivo_id>/<nombre_dispositivo>', methods=['DELETE'])
def eliminar_dispositivo(user_id, nombre_dispositivo, dispositivo_id):
    """Elimina un dispositivo de la lista de dispositivos registrados del usuario

    Elimina un dispositivo de la lista de dispositivos registrados del usuario # noqa: E501

    :param user_id: ID del usuario
    :type user_id: int
    :param dispositivo_id: ID del usuario
    :type dispositivo_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    dispositivo_usuario_db = DispositivosUsuarioDB.query.filter_by(user_id=user_id, dispositivo_id=dispositivo_id, nombre_dispositivo=nombre_dispositivo).first()

    if dispositivo_usuario_db is not None:
        numero_dispositivos = DispositivosUsuarioDB.query.filter_by(user_id=user_id).count()
        if numero_dispositivos == 1:
            return jsonify({"message": "No se puede eliminar el único dispositivo registrado", "status": "error"}), 400

        db.session.delete(dispositivo_usuario_db)
        db.session.commit()
        return jsonify({"message": "Dispositivo eliminado con éxito", "status": "success"}), 200
    else:
        return jsonify({"message": "El dispositivo no existe", "status": "error"}), 404

@app.route('/usuarios/<user_id>/dispositivos', methods=['GET'])
def obtener_dispositivos(user_id):  # noqa: E501
    """Obtiene la lista de dispositivos registrados por el usuario

    Obtiene la lista de dispositivos registrados por el usuario # noqa: E501

    :param user_id: ID del usuario
    :type user_id: int

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    dispositivos_usuarios_db = DispositivosUsuarioDB.query.filter_by(user_id=user_id).all()
    dispositivos = []
    if dispositivos_usuarios_db is not None:
        for dispositivo_usuario_db in dispositivos_usuarios_db:
            dispositivos_aux =DispositivoDB.query.filter_by(dispositivo_id=dispositivo_usuario_db.dispositivo_id).first() # Tipo de dispositivo
            disp= {
                "nombre": dispositivo_usuario_db.nombre_dispositivo,
                "tipo": dispositivos_aux.tipo_dispositivo,
                "dispositivo_id": dispositivo_usuario_db.dispositivo_id
            }
            dispositivos.append(disp)
     
    return jsonify(dispositivos), 200    

@app.route('/usuarios/<user_id>/dispositivos', methods=['POST'])
def crear_dispositivo(user_id):  # noqa: E501
    """Registra un nuevo dispositivo para el usuario

    Registra un nuevo dispositivo para el usuario # noqa: E501

    :param user_id: ID del usuario
    :type user_id: int
    :param nombre_dispositivo: Nombre del dispositivo
    :type nombre_dispositivo: str
    :param tipo_dispositivo: Tipo de dispositivo
    :type tipo_dispositivo: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if request.is_json:
        data = request.get_json()
        nombre_dispositivo = data.get('nombre_dispositivo')
        tipo_dispositivo = data.get('tipo_dispositivo')

        # Verificar si ya existe un dispositivo con la combinación de user_id, nombre_dispositivo y tipo_dispositivo
        dispositivo_existente = DispositivosUsuarioDB.query.filter_by(
            user_id=user_id,
            nombre_dispositivo=nombre_dispositivo,
            dispositivo_id=tipo_dispositivo
        ).first()

        if dispositivo_existente:
            return jsonify({"message": "Ya existe un dispositivo con los mismos datos", "status": "error"}), 400

        dispositivo = DispositivosUsuarioDB(
            user_id=user_id, 
            nombre_dispositivo=nombre_dispositivo, 
            dispositivo_id=tipo_dispositivo
        )
        
        db.session.add(dispositivo)
        db.session.commit()

        return jsonify({"message": "Dispositivo creado con éxito", "status": "success"}), 200
    else:
        return jsonify({"message": "Error en la creación del dispositivo", "status": "error"}), 404