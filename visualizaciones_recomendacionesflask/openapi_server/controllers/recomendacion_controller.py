# Se importa el fichero de configuración de los microservicios
import os, sys, requests
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(app_path)

from global_config import ContenidosConfig, UsuariosConfig

from openapi_server import app
from flask import jsonify, request

from openapi_server.models.recomendacion_pelicula_db import RecomendacionPeliculaDB
from openapi_server.models.recomendacion_serie_db import RecomendacionSerieDB

@app.route('/usuarios/<user_id>/perfiles/<perfil_id>/recomendaciones', methods=['PATCH'])
def actualizar_lista_recomendacion_perfil(user_id, perfil_id):
    """Actualiza una recomendación para un perfil

    Actualiza la lista de contenido de una recomendación para un perfil en específico

    :param user_id: ID del usuario especificado
    :type user_id: int
    :param perfil_id: ID del perfil especificado
    :type perfil_id: int

    :rtype: Union[Recomendacion, Tuple[Recomendacion, int], Tuple[Recomendacion, int, Dict[str, str]]
    """
    # Obtener el perfil con una petición al microservicio de usuario
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}")

    if response_perfil.status_code != 200:
        return jsonify({"message": "Perfil no encontrado"}), 404

    if request.is_json:
        recomendacion_update = request.get_json()

    if not recomendacion_update:
        return jsonify({"message": "Datos no válidos"}), 400

    # Recomendacion update tiene una lista actualizada de peliculas / series
    if 'peliculas_recomendadas' in recomendacion_update:
        recomendacion_pelicula = RecomendacionPeliculaDB.objects(id_perfil=perfil_id).first()
        recomendacion_pelicula.peliculas_recomendadas = recomendacion_update['peliculas_recomendadas']
        recomendacion_pelicula.save()

    if 'series_recomendadas' in recomendacion_update:
        recomendacion_serie = RecomendacionSerieDB.objects(id_perfil=perfil_id).first()
        recomendacion_serie.series_recomendadas = recomendacion_update['series_recomendadas']
        recomendacion_serie.save()

    return jsonify({"message": "Recomendaciones actualizadas correctamente"}), 200

@app.route('/usuarios/<user_id>/perfiles/<perfil_id>/recomendaciones', methods=['POST'])
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
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}")

    if response_perfil.status_code != 200:
        return jsonify({"message": "Perfil no encontrado"}), 404

    preferencias_perfil = response_perfil.json()["preferencias_contenido"]
    generos_perfil = preferencias_perfil["generos"]
    generos_perfil = [genero["id"] for genero in generos_perfil]

    # Se obtienen todas las películas y series
    lista_peliculas_api = requests.get(f"{ContenidosConfig.CONTENIDOS_BASE_URL}/peliculas")
    lista_series_api = requests.get(f"{ContenidosConfig.CONTENIDOS_BASE_URL}/series")

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
    
@app.route('/usuarios/<user_id>/perfiles/<perfil_id>/recomendaciones', methods=['DELETE'])
def eliminar_recomendacion_perfil(user_id, perfil_id):  # noqa: E501
    """Elimina una recomendación de un perfil

    Elimina una recomendación de un perfil # noqa: E501

    :param perfil_id: ID del perfil especificado
    :type perfil_id: int
    :param recomendacion_id: ID de la recomendacion especificada
    :type recomendacion_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    # Se comprueba si existe el perfil
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}")

    if response_perfil.status_code != 200:
        return jsonify({"message": "Perfil no encontrado"}), 404

    recomendaciones_pelicula = RecomendacionPeliculaDB.objects(id_perfil=perfil_id).first()
    recomendaciones_serie = RecomendacionSerieDB.objects(id_perfil=perfil_id).first()

    print(f"Recomendaciones Pelicula: {recomendaciones_pelicula}\n")

    if recomendaciones_pelicula:
        recomendaciones_pelicula.delete()
    if recomendaciones_serie:
        recomendaciones_serie.delete()

    return jsonify({"message": "Recomendaciones eliminadas correctamente"}), 200

@app.route('/usuarios/<user_id>/perfiles/<perfil_id>/recomendaciones', methods=['GET'])
def obtener_recomendaciones_perfil(user_id, perfil_id):
    """Obtiene una lista de las recomendaciones para el perfil"""
   
    recomendaciones_peliculas = RecomendacionPeliculaDB.objects(id_perfil=perfil_id)
    recomendaciones_series = RecomendacionSerieDB.objects(id_perfil=perfil_id)

    peliculas_recomendadas = []
    series_recomendadas = []

    for pelicula in recomendaciones_peliculas:
        if pelicula.id_perfil == int(perfil_id):  # Verificar perfil
            peliculas_recomendadas.extend(pelicula.peliculas_recomendadas)

    for serie in recomendaciones_series:
        if serie.id_perfil == int(perfil_id):  # Verificar perfil
            series_recomendadas.extend(serie.series_recomendadas)

    recomendaciones = {
        "peliculas": peliculas_recomendadas,
        "series": series_recomendadas
    }

    return jsonify(recomendaciones), 200

