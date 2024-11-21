# Se importa el fichero de configuración de los microservicios
import os, sys, requests
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(app_path)

from global_config import ContenidosConfig, UsuariosConfig

import connexion
from datetime import datetime
from bson import ObjectId
from flask import jsonify, request
from typing import Dict, Tuple, Union

from openapi_server.models.visualizacion_pelicula import VisualizacionPelicula  # noqa: E501
from openapi_server.models.visualizacion_capitulo import VisualizacionCapitulo  # noqa: E501
from openapi_server.models.visualizacion_pelicula_db import VisualizacionPeliculaDB
from openapi_server.models.visualizacion_capitulo_db import VisualizacionCapituloDB

from openapi_server import util
from openapi_server import app

@app.route('/usuario/<user_id>/perfil/<perfil_id>/visualizacion/<contenido_id>', methods=['PATCH'])
def actualizar_visualizacion_contenido_perfil(user_id, perfil_id, contenido_id):  # noqa: E501
    """Actualiza la visualización de un capítulo o película por un perfil

    Actualiza la visualización de un capítulo o película por un perfil

    :param perfil_id: ID del perfil especificado
    :type perfil_id: int
    :param visualizacion: ID del contenido a visualizar
    :type visualizacion: dict | bytes

    :rtype: Union[Visualizacion, Tuple[Visualizacion, int], Tuple[Visualizacion, int, Dict[str, str]]
    """
    # Se obtiene el perfil con una petición al microservicio de usuario
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuario/{user_id}/perfiles/{perfil_id}")

    if response_perfil.status_code != 200:
        return jsonify({"message": "Perfil no encontrado"}), 404

    # Se obtiene el objecto visualización a actualizar
    visualizacion = VisualizacionPeliculaDB.objects(id_perfil=perfil_id, pelicula_id=contenido_id).first()
    if visualizacion is None:
        visualizacion = VisualizacionCapituloDB.objects(id_perfil=perfil_id, capitulo_id=contenido_id).first()

    if visualizacion is None:
        return jsonify({"message": "Visualización no encontrada"}), 404

    # Se actualiza la fecha de visualización
    visualizacion.fecha_visualizacion = datetime.now()
    visualizacion.save()

    return jsonify({"message": "Visualización actualizada"}), 200


@app.route('/usuario/<user_id>/perfil/<perfil_id>/visualizacion', methods=['POST'])
def crear_visualizacion_contenido_perfil(user_id, perfil_id):  # noqa: E501
    """Inicia la visualización de un capítulo o película por un perfil

    Inicia la visualización de un capítulo o película por un perfil # noqa: E501

    :param perfil_id: ID del perfil especificado
    :type perfil_id: int
    :param visualizacion: ID del contenido a visualizar
    :type visualizacion: dict | bytes

    :rtype: Union[Visualizacion, Tuple[Visualizacion, int], Tuple[Visualizacion, int, Dict[str, str]]
    """
    # Se obtiene el perfil con una petición al microservicio de usuario
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuario/{user_id}/perfiles/{perfil_id}")

    if response_perfil.status_code != 200:
        return jsonify({"message": "Perfil no encontrado"}), 404

    # Se obtiene el contenido a visualizar
    es_capitulo = False
    visualizacion = request.get_json()

    print(f"Visualización: {visualizacion}\n\n")

    if "pelicula_id" in visualizacion:
        visualizacion_db = VisualizacionPeliculaDB(
            id_perfil=perfil_id,
            pelicula_id=visualizacion["pelicula_id"],
            fecha_visualizacion=datetime.now()
        )
    elif "serie_id" and "temporada_id" and "capitulo_id" in visualizacion:
        visualizacion_db = VisualizacionCapituloDB(
            id_perfil=perfil_id,
            serie_id=visualizacion["serie_id"],
            temporada_id=visualizacion["temporada_id"],
            capitulo_id=visualizacion["capitulo_id"],
            fecha_visualizacion=datetime.now()
        )
        es_capitulo = True
    else:
        return jsonify({"message": "Contenido no encontrado"}), 404

    # Se actualiza el historial de visualizaciones del perfil
    payload = {}
    if es_capitulo:
        payload = {
            "serie_id": visualizacion["serie_id"],
            "temporada_id": visualizacion["temporada_id"],
            "capitulo_id": visualizacion["capitulo_id"],
        }
    else:
        payload = {
            "pelicula_id": visualizacion["pelicula_id"]
        }

    response_historial = requests.post(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuario/{user_id}/perfiles/{perfil_id}/historial", json=payload)

    if response_historial.status_code != 201:
        return jsonify({"message": "Error al actualizar el historial de visualizaciones"}), 500

    # Se guarda la visualización en la base de datos
    visualizacion_db.save()

    return jsonify({"message": "Visualización creada"}), 201

@app.route('/usuario/<user_id>/perfil/<perfil_id>/visualizacion', methods=['DELETE'])
def borrar_visualizaciones_perfil(user_id, perfil_id):
    """Borra todas las visualizaciones de un perfil

    Borra todas las visualizaciones de un perfil

    :param perfil_id: ID del perfil especificado
    :type perfil_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    # Se obtienen todas las visualizaciones del perfil
    visualizaciones_pelicula = VisualizacionPeliculaDB.objects().filter(id_perfil=perfil_id)
    visualizaciones_capitulo = VisualizacionCapituloDB.objects().filter(id_perfil=perfil_id)

    # Se borran las visualizaciones
    for visualizacion in visualizaciones_pelicula:
        visualizacion.delete()

    for visualizacion in visualizaciones_capitulo:
        visualizacion.delete()

    return jsonify({"message": "Visualizaciones borradas"}), 200

@app.route('/usuario/<user_id>/perfil/<perfil_id>/visualizacion/<contenido_id>', methods=['DELETE'])
def borrar_visualizacion_perfil(user_id, perfil_id, contenido_id):  # noqa: E501
    """Borra la visualización de la película por un perfil

    Borra el progreso de la visualización de la película por un perfil # noqa: E501

    :param perfil_id: ID del perfil específicado
    :type perfil_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    # Se comprueba si el contenido_id corresponde a una película o a un capítulo
    cap = False
    visualizacion = VisualizacionPeliculaDB.objects(id_perfil=perfil_id, pelicula_id=contenido_id).first()

    if visualizacion is None:
        cap = True
        visualizacion = VisualizacionCapituloDB.objects(id_perfil=perfil_id, capitulo_id=contenido_id).first()

    if visualizacion is None:
        return jsonify({"message": "Visualización no encontrada"}), 404

    # Se actualiza el historial de visualizaciones del perfil
    visualizacion_api = visualizacion.to_api_model()
    payload = {}
    if cap:
        payload = {
            "serie_id": visualizacion_api.serie_id,
            "temporada_id": visualizacion_api.temporada_id,
            "capitulo_id": visualizacion_api.capitulo_id
        }
    else:
        payload = {
            "pelicula_id": visualizacion_api.pelicula_id
        }

    response_historial = requests.delete(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuario/{user_id}/perfiles/{perfil_id}/historial", json=payload)

    if response_historial.status_code != 200:
        return jsonify({"message": "Error al actualizar el historial de visualizaciones"}), 500

    # Se borra la visualización
    visualizacion.delete()

    return jsonify({"message": "Visualización borrada"}), 200

@app.route('/contenido/<contenido_id>/visualizacion', methods=['GET'])
def listar_visualizaciones_contenido(contenido_id):  # noqa: E501
    """Lista de perfiles que han visto el contenido especificado

    Lista de perfiles que han visto el contenido especificado. # noqa: E501

    :param contenido_id: ID del perfil a obtener
    :type contenido_id: int

    :rtype: Union[List[Perfil], Tuple[List[Perfil], int], Tuple[List[Perfil], int, Dict[str, str]]
    """
    # Contenido_id puede ser una película o un capítulo
    visualizaciones = VisualizacionPeliculaDB.objects().filter(pelicula_id=ObjectId(contenido_id))

    if len(visualizaciones) == 0:
        visualizaciones = VisualizacionCapituloDB.objects().filter(capitulo_id=ObjectId(contenido_id))

    if len(visualizaciones) == 0:
        return jsonify({"message": "Visualización no encontrada"}), 404

    perfiles = []
    for visualizacion in visualizaciones:
        perfiles.append(visualizacion.to_api_model().id_perfil)

    return jsonify(perfiles), 200

@app.route('/usuario/<user_id>/perfil/<perfil_id>/visualizacion', methods=['GET'])
def listar_visualizaciones_perfil(user_id, perfil_id):  # noqa: E501
    """Historial de un perfil en específico

    Obtiene una lista de todos los capítulos o películas visualizados o en progreso por el perfil especificado. # noqa: E501

    :param perfil_id: ID del perfil a obtener
    :type perfil_id: int

    :rtype: Union[List[Visualizacion], Tuple[List[Visualizacion], int], Tuple[List[Visualizacion], int, Dict[str, str]]
    """
    # Se comprueba si existe el perfil
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuario/{user_id}/perfiles/{perfil_id}")

    if response_perfil.status_code != 200:
        return jsonify({"message": "Perfil no encontrado"}), 404

    visualizaciones_pelicula = VisualizacionPeliculaDB.objects(id_perfil=perfil_id)
    visualizaciones_capitulo = VisualizacionCapituloDB.objects(id_perfil=perfil_id)

    visualizaciones = []
    for visualizacion in visualizaciones_pelicula:
        visualizaciones.append(visualizacion.to_api_model())

    for visualizacion in visualizaciones_capitulo:
        visualizaciones.append(visualizacion.to_api_model())

    return jsonify(visualizaciones), 200


def obtener_visualizacion_capitulo_perfil(perfil_id, capitulo_id):  # noqa: E501
    """Obtiene el capítulo en visualización del perfil especificado

    Obtiene el capítulo en visualización por el perfil especificado. # noqa: E501

    :param perfil_id: ID del perfil a obtener
    :type perfil_id: int
    :param capitulo_id: ID del perfil a obtener
    :type capitulo_id: int

    :rtype: Union[List[Capitulo], Tuple[List[Capitulo], int], Tuple[List[Capitulo], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_visualizacion_pelicula_perfil(perfil_id, pelicula_id):  # noqa: E501
    """Obtiene la película visualizada por el perfil especificado

    Obtiene la película en visualización por el perfil especificado. # noqa: E501

    :param perfil_id: ID del perfil a obtener
    :type perfil_id: int
    :param pelicula_id: ID del perfil a obtener
    :type pelicula_id: int

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    return 'do some magic!'
