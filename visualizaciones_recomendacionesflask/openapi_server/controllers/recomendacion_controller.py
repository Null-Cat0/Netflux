# Se importa el fichero de configuración de los microservicios
import os, sys, requests
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(app_path)

from global_config import ContenidosConfig, UsuariosConfig

import connexion
from flask import jsonify, request
from typing import Dict, Tuple, Union

from openapi_server.models.recomendacion_pelicula import RecomendacionPelicula
from openapi_server.models.recomendacion_serie import RecomendacionSerie  #
from openapi_server.models.recomendacion_pelicula_db import RecomendacionPeliculaDB
from openapi_server.models.recomendacion_serie_db import RecomendacionSerieDB

from openapi_server import util

from openapi_server import app

@app.route('/usuario/<user_id>/perfil/<perfil_id>/recomendacion', methods=['POST'])
def crear_recomendacion_perfil(user_id, perfil_id):  # noqa: E501
    """Crea una recomendación para un perfil

    Crea una recomendación para un perfil en específico # noqa: E501

    :param user_id: ID del usuario especificado
    :type user_id: int
    :param perfil_id: ID del perfil especificado
    :type perfil_id: int

    :rtype: Union[Recomendacion, Tuple[Recomendacion, int], Tuple[Recomendacion, int, Dict[str, str]]
    """

    # Obtener el perfil con una petición al microservicio de usuario
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuario/{user_id}/perfiles/{perfil_id}")

    if response_perfil.status_code != 200:
        return jsonify({"message": "Perfil no encontrado"}), 404

    preferencias_perfil = response_perfil.json()["preferencias_contenido"]
    generos_perfil = preferencias_perfil["generos"]
    generos_perfil = [genero["id"] for genero in generos_perfil]

    # Se obtienen todas las películas y series
    lista_peliculas_api = requests.get(f"{ContenidosConfig.CONTENIDOS_BASE_URL}/listar_peliculas")
    lista_series_api = requests.get(f"{ContenidosConfig.CONTENIDOS_BASE_URL}/listar_series")

    if lista_peliculas_api.status_code != 200 or lista_series_api.status_code != 200:
        return jsonify({"message": "Error al obtener las películas o series"}), 500

    # Se filtran las películas y series por los géneros del perfil
    lista_peliculas_genero = []
    for pelicula in lista_peliculas_api.json():
        for genero in pelicula["genero"]:
            print(f"Genero: {genero}\n")
            if genero["id"] in generos_perfil:
                lista_peliculas_genero.append(pelicula['id'])
                break

    lista_series_genero = []
    for serie in lista_series_api.json():
        for genero in serie["genero"]:
            if genero["id"] in generos_perfil:
                lista_series_genero.append(serie['id'])
                break

    # Se crea el objecto recomendacion con las películas y series
    recomendacion_pelicula = RecomendacionPeliculaDB(
        id_perfil=perfil_id,
        peliculas_recomendadas=lista_peliculas_genero
    )
    recomendacion_serie = RecomendacionSerieDB(
        id_perfil=perfil_id,
        series_recomendadas=lista_series_genero
    )

    # Se guardan las recomendaciones en la base de datos
    recomendacion_pelicula.save()
    recomendacion_serie.save()

    return jsonify({"message": "Recomendaciones creadas correctamente"}), 201
    
@app.route('/usuario/<user_id>/perfil/<perfil_id>/recomendacion', methods=['DELETE'])
def eliminar_recomendacion_perfil(user_id, perfil_id):  # noqa: E501
    """Elimina una recomendación en específico de un perfil

    Elimina una recomendación en específico de un perfil # noqa: E501

    :param perfil_id: ID del perfil especificado
    :type perfil_id: int
    :param recomendacion_id: ID de la recomendacion especificada
    :type recomendacion_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    # Se comprueba si existe el perfil
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuario/{user_id}/perfiles/{perfil_id}")

    if response_perfil.status_code != 200:
        return jsonify({"message": "Perfil no encontrado"}), 404

    try:
        recomendaciones_pelicula = RecomendacionPeliculaDB.objects.get(id_perfil=perfil_id)
        recomendaciones_serie = RecomendacionSerieDB.objects.get(id_perfil=perfil_id)

        if recomendaciones_pelicula:
            recomendaciones_pelicula.delete()
        if recomendaciones_serie:
            recomendaciones_serie.delete()

    except RecomendacionPeliculaDB.DoesNotExist:
        raise RecomendacionPelicula.DoesNotExist

    return jsonify({"message": "Recomendaciones eliminadas correctamente"}), 200

@app.route('/usuario/<user_id>/perfil/<perfil_id>/recomendacion', methods=['GET'])
def obtener_recomendaciones_perfil(user_id, perfil_id):  # noqa: E501
    """Obtiene una lista de las recomendaciones para el perfil

    Obtiene una lista de las recomendaciones para el perfil # noqa: E501

    :param perfil_id: ID del perfil especificado
    :type perfil_id: int

    :rtype: Union[List[Recomendacion], Tuple[List[Recomendacion], int], Tuple[List[Recomendacion], int, Dict[str, str]]
    """
    recomendaciones_pelicula = RecomendacionPeliculaDB.objects.get(id_perfil=perfil_id) 
    recomendaciones_serie = RecomendacionSerieDB.objects.get(id_perfil=perfil_id)

    rpl = [rp.to_api_model() for rp in recomendaciones_pelicula]
    rsl = [rs.to_api_model() for rs in recomendaciones_serie]

    # Se junta la información de las recomendaciones de películas y series
    recomendaciones = {
        "peliculas": rpl.peliculas_recomendadas or [],
        "series": rsl.series_recomendadas or []
    }

    return jsonify(recomendaciones), 200
