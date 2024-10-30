import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.dispositivo_db import DispositivoDB
from openapi_server.models.dispositivos_usuario_db import DispositivosUsuarioDB

from openapi_server import app

from openapi_server.models.actualizar_dispositivos_request import ActualizarDispositivosRequest  # noqa: E501
from openapi_server import util
from flask import request, jsonify

def actualizar_dispositivos(user_id, actualizar_dispositivos_request):  # noqa: E501
    """Actualiza un dispositivo a la lista de dispositivos registrados del usuario

    Actualiza un dispositivo a la lista de dispositivos registrados del usuario # noqa: E501

    :param user_id: ID del usuario
    :type user_id: int
    :param actualizar_dispositivos_request: ID del dispositivo a actualizar
    :type actualizar_dispositivos_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        actualizar_dispositivos_request = ActualizarDispositivosRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def eliminar_dispositivo(user_id, dispositivo_id):  # noqa: E501
    """Elimina un dispositivo de la lista de dispositivos registrados del usuario

    Elimina un dispositivo de la lista de dispositivos registrados del usuario # noqa: E501

    :param user_id: ID del usuario
    :type user_id: int
    :param dispositivo_id: ID del usuario
    :type dispositivo_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'

@app.route('/usuario/<user_id>/dispositivos', methods=['GET'])
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
                "tipo": dispositivos_aux.tipo_dispositivo
                }
            dispositivos.append(disp)
     
    return jsonify(dispositivos), 200    

    return 'do some magic!'
