import requests
from openapi_server.config import UsuariosConfig

from openapi_server import app
from flask import jsonify, request

from openapi_server.models.visualizacion_pelicula_db import VisualizacionPeliculaDB
from openapi_server.models.visualizacion_capitulo_db import VisualizacionCapituloDB

@app.route('/usuarios/<user_id>/perfiles/<perfil_id>/visualizaciones/<contenido_id>', methods=['PATCH'])
def actualizar_visualizacion_contenido_perfil(user_id, perfil_id, contenido_id):  # noqa: E501
    # Se obtiene el perfil con una petición al microservicio de usuario
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}")

    if response_perfil.status_code != 200:
        return jsonify({"message": "Perfil no encontrado"}), 404

    # Se obtiene el objecto visualización a actualizar
    visualizacion = VisualizacionPeliculaDB.objects(id_perfil=perfil_id, pelicula_id=contenido_id).first()
    if visualizacion is None:
        visualizacion = VisualizacionCapituloDB.objects(id_perfil=perfil_id, capitulo_id=contenido_id).first()

    if visualizacion is None:
        return jsonify({"message": "Visualización no encontrada"}), 404

    visualizacion.save()

    return jsonify({"message": "Visualización actualizada"}), 200

@app.route('/usuarios/<user_id>/perfiles/<perfil_id>/visualizaciones', methods=['POST'])
def crear_visualizacion_contenido_perfil(user_id, perfil_id):  # noqa: E501
    # Se obtiene el perfil con una petición al microservicio de usuario
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}")

    if response_perfil.status_code != 200:
        return jsonify({"message": "Perfil no encontrado"}), 404

    # Se obtiene el contenido a visualizar
    es_capitulo = False
    visualizacion = request.get_json()

    if "pelicula_id" in visualizacion:
        visualizacion_db = VisualizacionPeliculaDB(
            id_perfil=perfil_id,
            pelicula_id=visualizacion["pelicula_id"],
        )
    elif "serie_id" and "temporada_id" and "capitulo_id" in visualizacion:
        visualizacion_db = VisualizacionCapituloDB(
            id_perfil=perfil_id,
            serie_id=visualizacion["serie_id"],
            temporada_id=visualizacion["temporada_id"],
            capitulo_id=visualizacion["capitulo_id"],
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

    response_historial = requests.post(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}/historial", json=payload)

    if response_historial.status_code != 201:
        return jsonify({"message": "Error al actualizar el historial de visualizaciones"}), 500

    # Se guarda la visualización en la base de datos
    visualizacion_db.save()

    return jsonify({"message": "Visualización creada"}), 201

@app.route('/usuarios/<user_id>/perfiles/<perfil_id>/visualizaciones', methods=['DELETE'])
def borrar_visualizaciones_perfil(user_id, perfil_id):
    # Se obtienen todas las visualizaciones del perfil
    visualizaciones_pelicula = VisualizacionPeliculaDB.objects().filter(id_perfil=perfil_id)
    visualizaciones_capitulo = VisualizacionCapituloDB.objects().filter(id_perfil=perfil_id)

    # Se borran las visualizaciones
    for visualizacion in visualizaciones_pelicula:
        visualizacion.delete()

    for visualizacion in visualizaciones_capitulo:
        visualizacion.delete()

    return jsonify({"message": "Visualizaciones borradas"}), 200

@app.route('/usuarios/<user_id>/perfiles/<perfil_id>/visualizaciones/<contenido_id>', methods=['DELETE'])
def borrar_visualizacion_perfil(user_id, perfil_id, contenido_id):  # noqa: E501
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

    response_historial = requests.delete(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}/historial", json=payload)

    if response_historial.status_code != 200:
        return jsonify({"message": "Error al actualizar el historial de visualizaciones"}), 500

    # Se borra la visualización
    visualizacion.delete()

    return jsonify({"message": "Visualización borrada"}), 200

@app.route('/usuarios/<user_id>/perfiles/<perfil_id>/visualizaciones', methods=['GET'])
def listar_visualizaciones_perfil(user_id, perfil_id):  # noqa: E501
    # Se comprueba si existe el perfil
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}")

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

@app.route('/usuarios/<user_id>/perfiles/<perfil_id>/visualizaciones/capitulos/<capitulo_id>', methods=['GET'])
def obtener_visualizacion_capitulo_perfil(user_id, perfil_id, capitulo_id):  # noqa: E501
    # Se comprueba si existe el perfil
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}")

    if response_perfil.status_code != 200:
        return jsonify({"message": "Perfil no encontrado"}), 404

    # Se intenta obtener la visualización del capítulo o película
    visualizacion = VisualizacionCapituloDB.objects(id_perfil=perfil_id, capitulo_id=capitulo_id).first()

    if visualizacion is None:
        return jsonify({"message": "Visualización del capítulo no encontrada"}), 404

    return jsonify(visualizacion.to_api_model()), 200

@app.route('/usuarios/<user_id>/perfiles/<perfil_id>/visualizaciones/peliculas/<pelicula_id>', methods=['GET'])
def obtener_visualizacion_pelicula_perfil(user_id, perfil_id, pelicula_id):  # noqa: E501
    # Se comprueba si existe el perfil
    response_perfil = requests.get(f"{UsuariosConfig.USUARIOS_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}")

    if response_perfil.status_code != 200:
        return jsonify({"message": "Perfil no encontrado"}), 404

    # Se intenta obtener la visualización de la película
    visualizacion = VisualizacionPeliculaDB.objects(id_perfil=perfil_id, pelicula_id=pelicula_id).first()

    if visualizacion is None:
        return jsonify({"message": "Visualización de la película no encontrada"}), 404

    return jsonify(visualizacion.to_api_model()), 200