# Se importa el fichero de configuración de los microservicios
import os, sys, requests

from openapi_server.config import ContenidosConfig, VisualizacionesConfig

from openapi_server import app, db
from flask import request, jsonify
from datetime import datetime

from openapi_server.models.perfil import Perfil
from openapi_server.models.perfil_db import PerfilDB

from openapi_server.models.preferencias_contenido_db import PreferenciasContenidoDB
from openapi_server.models.genero_preferencias_db import GeneroPreferenciasDB
from openapi_server.models.historial_perfil_db import HistorialPerfilDB
from openapi_server.models.lista_perfil_db import ListaPerfilDB

# Método auxiliar para eliminar las recomendaciones y visualizaciones de un perfil
def eliminar_datos_perfil(user_id, perfil_id):
    # Se han de eliminar las recomendaciones y visualizaciones del perfil
    recomendaciones_perfil = requests.delete(f"{VisualizacionesConfig.VISUALIZACIONES_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}/recomendaciones")
    if recomendaciones_perfil.status_code != 200:
        return jsonify({"message": "Error al eliminar las recomendaciones del perfil"}), 500

    visualizaciones_perfil = requests.delete(f"{VisualizacionesConfig.VISUALIZACIONES_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}/visualizaciones")
    if visualizaciones_perfil.status_code != 200:
        return jsonify({"message": "Error al eliminar las visualizaciones del perfil"}), 500

@app.route('/usuarios/<user_id>/perfiles/<profile_id>', methods=['PUT'])
def actualizar_perfil_usuario(user_id, profile_id):
    # Verifica si la solicitud contiene JSON
    if not request.is_json:
        return jsonify({"message": "La solicitud debe contener datos JSON"}), 400

    perfil_data = request.get_json()
    perfil_api = Perfil.from_dict(perfil_data)
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()

    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil a actualizar", "status": "error"}), 404

    # Actualiza los campos del perfil
    perfil_db.nombre = perfil_api.nombre
    perfil_db.foto_perfil = perfil_api.foto_perfil

    # Se gestionan las preferencias de contenido
    preferencias_db = PreferenciasContenidoDB.query.filter_by(perfil_id=perfil_db.perfil_id).first()

    ## Se actualizan las preferencias de contenido
    preferencias_db.subtitulos = perfil_api.preferencias_contenido.subtitulos
    preferencias_db.idioma_audio = perfil_api.preferencias_contenido.idioma_audio

    ## Se eliminan los géneros anteriores
    GeneroPreferenciasDB.query.filter_by(preferencias_id=preferencias_db.preferencias_id).delete()

    ## Se añaden los nuevos géneros
    genero_preferencias_db = GeneroPreferenciasDB.query.filter_by(preferencias_id=preferencias_db.preferencias_id).all()
    for gpdb in genero_preferencias_db:
        db.session.delete(gpdb)

    generos_name_list = perfil_api.preferencias_contenido.generos
    generos_response = requests.get(f'{ContenidosConfig.CONTENIDOS_BASE_URL}/generos')
    if generos_response.status_code != 200:
        return jsonify({"message": "Error al obtener los géneros"}), 500

    generos = generos_response.json()
    for g in generos:
        if g['nombre'] in generos_name_list:
            genero_preferencias_db = GeneroPreferenciasDB(
                preferencias_id=preferencias_db.preferencias_id,
                genero_id=g['id']
            )
            db.session.add(genero_preferencias_db)

    # Se guardan los cambios en la base de datos
    db.session.commit()

    # Se actualizan las recomendaciones al perfil
    recomendaciones_perfil = requests.delete(f"{VisualizacionesConfig.VISUALIZACIONES_BASE_URL}/usuarios/{perfil_db.user_id}/perfiles/{perfil_db.perfil_id}/recomendaciones")

    if recomendaciones_perfil.status_code != 200:
        return jsonify({"message": "Error al eliminar las recomendaciones del perfil"}), 500

    recomendaciones_perfil = requests.post(f"{VisualizacionesConfig.VISUALIZACIONES_BASE_URL}/usuarios/{perfil_db.user_id}/perfiles/{perfil_db.perfil_id}/recomendaciones")

    if recomendaciones_perfil.status_code != 201:
        return jsonify({"message": "Error al crear las recomendaciones del perfil"}), 500

    return jsonify(perfil_api.serialize()), 200

@app.route('/usuarios/<user_id>/perfiles', methods=['DELETE'])
def borrar_perfiles_usuario(user_id):  # noqa: E501
    perfiles_db = PerfilDB.query.filter_by(user_id=user_id).all()
    if perfiles_db is None:
        return jsonify({"message": "No se ha encontrado el perfil a eliminar"}, 404)

    for perfil_db in perfiles_db:
        # Se han de eliminar las recomendaciones y visualizaciones del perfil
        eliminar_datos_perfil(perfil_db.user_id, perfil_db.perfil_id)

    return jsonify({"message": "Datos de los perfiles eliminados con éxito", "status": "success"}), 200

@app.route('/usuarios/<user_id>/perfiles/<profile_id>', methods=['DELETE'])
def borrar_perfil_usuario(user_id, profile_id):  # noqa: E501
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is not None:
        # Se han de eliminar las recomendaciones y visualizaciones del perfil
        eliminar_datos_perfil(perfil_db.user_id, perfil_db.perfil_id)

        db.session.delete(perfil_db)
        db.session.commit()
        return jsonify({"message": "Perfil eliminado con éxito", "status": "success"}), 200
    else:
        return jsonify({"message": "No se ha podido eliminar el perfil", "status": "error"}), 404

@app.route('/usuarios/<user_id>/perfiles', methods=['POST'])
def crear_perfil(user_id):  # noqa: E501
    if request.is_json:
        perfil_api = Perfil.from_dict(request.get_json())  # noqa: E501

    # Obtener el campo 'foto_perfil', si no existe, usar 'netflux_rojo.png'
    foto_perfil = perfil_api.foto_perfil or 'netflux_rojo.png'

    # Validar que la imagen es una de las permitidas
    imagenes_permitidas = ['netflux_amarillo.png', 'netflux_azul.png', 'netflux_rojo.png', 'netflux_verde.png']
    if foto_perfil not in imagenes_permitidas:
        return jsonify({"message": "Imagen no válida.", "status": "error"}), 400

    if (perfil_api):
        perfil_db = perfil_api.to_db_model()
        db.session.add(perfil_db)
        db.session.commit()

        preferencias_api = perfil_api.preferencias_contenido
        preferencias_api.perfil_id = perfil_db.perfil_id
        preferencias_db = preferencias_api.to_db_model() 

        db.session.add(preferencias_db)
        db.session.commit()

        generos_name_list = preferencias_api.generos or []
        generos_response = requests.get(f'{ContenidosConfig.CONTENIDOS_BASE_URL}/generos')
        if generos_response.status_code == 200:
            generos = generos_response.json()
            for genero in generos:
                if genero['nombre'] in generos_name_list:
                    genero_preferencias_db = GeneroPreferenciasDB(preferencias_id=preferencias_db.preferencias_id, genero_id=genero['id'])
                    db.session.add(genero_preferencias_db)
            db.session.commit()
        else:
            return jsonify({"message": "Error al obtener los géneros"}), 500

        # Se crean recomendaciones al perfil
        recomendaciones_perfil = requests.post(f"{VisualizacionesConfig.VISUALIZACIONES_BASE_URL}/usuarios/{perfil_db.user_id}/perfiles/{perfil_db.perfil_id}/recomendaciones")

        if recomendaciones_perfil.status_code != 201:
            return jsonify({"message": "Error al crear la recomendaciones del perfil"}), 500

        return jsonify(perfil_api.serialize()), 201

    else:
        return jsonify({"message": "Ha habido un error con su solicitud, inténtelo de nuevo más tarde", "status": "error"}), 404
 
@app.route('/usuarios/<user_id>/perfiles/<profile_id>/historial', methods=['GET'])
def obtener_historial_perfil(user_id, profile_id):  # noqa: E501
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404
    
    historial_db = HistorialPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id).all()
    lista_capitulos = []
    lista_peliculas = []

    for h in historial_db:
        if (h.es_capitulo):
            lista_capitulos.append(h.contenido)
        else:
            lista_peliculas.append(h.contenido)

    # Ahora se hace la petición al microservicio de contenidos para obtener los datos de las series y películas
    response_capitulos = requests.get(f'{ContenidosConfig.CONTENIDOS_BASE_URL}/obtener_lista_capitulos', json=lista_capitulos)

    # Se añade la fecha de visualización a los capítulos
    if response_capitulos.status_code == 200:
        capitulos = response_capitulos.json()
        for c in capitulos:
            c['fecha_visualizacion'] = HistorialPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id, contenido=c['capitulo_id']).first().fecha_visualizacion
    else:
        return jsonify({"message": "No se ha podido obtener la lista de series", "status": "error"}), 404

    response_peliculas = requests.get(f'{ContenidosConfig.CONTENIDOS_BASE_URL}/obtener_lista_peliculas', json=lista_peliculas)

    # Se añade la fecha de visualización a las películas
    if response_peliculas.status_code == 200:
        peliculas = response_peliculas.json()
        for p in peliculas:
            p['fecha_visualizacion'] = HistorialPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id, contenido=p['id']).first().fecha_visualizacion
    else:
        return jsonify({"message": "No se ha podido obtener la lista de películas", "status": "error"}), 404

    return jsonify({"capitulos": capitulos, "peliculas": peliculas}), 200

@app.route('/usuarios/<user_id>/perfiles/<profile_id>/historial', methods=['POST'])
def agregar_contenido_historial(user_id, profile_id):
    # Verifica si la solicitud contiene JSON
    if request.is_json:
        contenido_json = request.get_json()

    # Buscamos el perfil en la base de datos
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404

    # Comprueba si el contenido es un capitulo o una película y hace la petición correspondiente
    cap = False
    if "pelicula_id" in contenido_json:
        pelicula_id = contenido_json["pelicula_id"]
        response_contenido = requests.get(f'{ContenidosConfig.CONTENIDOS_BASE_URL}/peliculas/{pelicula_id}')

    elif "serie_id" and "temporada_id" and "capitulo_id" in contenido_json:
        serie_id = contenido_json["serie_id"]
        temporada_id = contenido_json["temporada_id"]
        capitulo_id = contenido_json["capitulo_id"]

        response_contenido = requests.get(f'{ContenidosConfig.CONTENIDOS_BASE_URL}/series/{serie_id}/temporadas/{temporada_id}/capitulos/{capitulo_id}')
        cap = True

    else:
        return jsonify({"message": "La solicitud debe contener un capítulo o una película"}), 400

    if response_contenido.status_code != 200:
        return jsonify({"message": "No se ha encontrado el contenido", "status": "error"}), 404

    # Comprobar si el contenido ya está en el historial
    if not cap:
        historial_db = HistorialPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id, contenido=pelicula_id).first()
    else:
        historial_db = HistorialPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id, contenido=capitulo_id).first()

    if historial_db is not None:
        return jsonify({"message": "El contenido ya está en el historial", "status": "error"}), 409

    # Creamos el objeto HistorialPerfilDB
    historial_db = HistorialPerfilDB(
        perfil_id=perfil_db.perfil_id,
        contenido=pelicula_id if not cap else capitulo_id,
        es_capitulo=cap
    )
    db.session.add(historial_db)
    db.session.commit()

    return jsonify({"message": "Contenido añadido al historial", "status": "success"}), 201

@app.route('/usuarios/<user_id>/perfiles/<perfil_id>/historial/<contenido_id>', methods=['PATCH'])
def actualizar_contenido_historial(user_id, perfil_id, contenido_id):
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=perfil_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404

    historial_db = HistorialPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id, contenido=contenido_id).first()

    if historial_db is None:
        return jsonify({"message": "No se ha encontrado el contenido en el historial", "status": "error"}), 404

    historial_db.fecha_visualizacion = datetime.now()
    db.session.commit()

    return jsonify({"message": "Fecha de visualización actualizada", "status": "success"}), 200

@app.route('/usuarios/<user_id>/perfiles/<profile_id>/historial', methods=['DELETE'])
def eliminar_contenido_historial(user_id, profile_id):
    if not request.is_json:
        return jsonify({"message": "La solicitud debe contener un JSON"}), 400

    contenido_json = request.get_json()

    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404

    if "pelicula_id" in contenido_json:
        contenido_id = contenido_json["pelicula_id"]

    elif "serie_id" and "temporada_id" and "capitulo_id" in contenido_json:
        contenido_id = contenido_json["capitulo_id"]

    else:
        return jsonify({"message": "La solicitud debe contener un capítulo o una película"}), 400

    historial_db = HistorialPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id, contenido=contenido_id).first()

    if historial_db is None:
        return jsonify({"message": "No se ha encontrado el contenido en el historial", "status": "error"}), 404

    db.session.delete(historial_db)
    db.session.commit()

    return jsonify({"message": "Contenido eliminado del historial", "status": "success"}), 200

@app.route('/usuarios/<user_id>/perfiles/<profile_id>/lista', methods=['GET'])
def obtener_lista_perfil(user_id, profile_id):  # noqa: E501
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404
    
    lista_perfil_db = ListaPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id).all()
    lista_series = []
    lista_peliculas = []

    for h in lista_perfil_db:
        if (h.es_serie):
            lista_series.append(h.contenido)
        else:
            lista_peliculas.append(h.contenido)

    # Ahora se hace la petición al microservicio de contenidos para obtener los datos de las series y películas
    response_series = requests.get(f'{ContenidosConfig.CONTENIDOS_BASE_URL}/obtener_lista_series', json=lista_series)

    if response_series.status_code != 200:
        return jsonify({"message": "No se ha podido obtener la lista de series", "status": "error"}), 404

    response_peliculas = requests.get(f'{ContenidosConfig.CONTENIDOS_BASE_URL}/obtener_lista_peliculas', json=lista_peliculas)

    if response_peliculas.status_code != 200:
        return jsonify({"message": "No se ha podido obtener la lista de películas", "status": "error"}), 404

    series = response_series.json()
    peliculas = response_peliculas.json()

    return jsonify({"series": series, "peliculas": peliculas}), 200

@app.route('/usuarios/<user_id>/perfiles/<profile_id>/lista/<contenido_id>', methods=['POST'])
def agregar_contenido_lista(user_id, profile_id, contenido_id):
    # Buscamos el perfil en la base de datos
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404

    # Buscamos el contenido en la base de datos
    ## Hay que ver si es una serie o una película
    response_serie = requests.get(f'{ContenidosConfig.CONTENIDOS_BASE_URL}/series/{contenido_id}')
    if response_serie.status_code == 200:
        contenido_db = response_serie.json()
        es_serie = True
    else:
        response_pelicula = requests.get(f'{ContenidosConfig.CONTENIDOS_BASE_URL}/peliculas/{contenido_id}')
        if response_pelicula.status_code == 200:
            contenido_db = response_pelicula.json()
            es_serie = False
        else:
            return jsonify({"message": "No se ha encontrado el contenido", "status": "error"}), 404

    # Comprobar si el contenido ya está en la lista
    lista_perfil_db = ListaPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id, contenido=contenido_id).first()

    if lista_perfil_db is not None:
        return jsonify({"message": "El contenido ya está en la lista", "status": "warning"}), 409

    # Creamos el objeto ListaPerfilDB
    lista_perfil_db = ListaPerfilDB(
        perfil_id=perfil_db.perfil_id,
        contenido=contenido_db['id'],
        es_serie=es_serie
    )
    db.session.add(lista_perfil_db)
    db.session.commit()

    return jsonify({"message": "Contenido añadido a la lista", "status": "success"}), 201

@app.route('/usuarios/<user_id>/perfiles/<profile_id>/lista/<contenido_id>', methods=['DELETE'])
def eliminar_contenido_lista(user_id, profile_id, contenido_id):
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404

    lista_db = ListaPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id, contenido=contenido_id).first()
    if lista_db is None:
        return jsonify({"message": "No se ha encontrado el contenido en la lista", "status": "error"}), 404

    db.session.delete(lista_db)
    db.session.commit()

    return jsonify({"message": "Contenido eliminado de la lista", "status": "success"}), 200

@app.route('/usuarios/<user_id>/perfiles/<profile_id>', methods=['GET'])
def obtener_perfil_usuario(user_id, profile_id):  # noqa: E501    
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is not None:
        perfil = perfil_db.to_api_model()
        if perfil is None:
            return jsonify({"message": "No hay perfiles disponibles", "status": "error"}), 404
        else:
            return jsonify(perfil.serialize()), 200

@app.route('/usuarios/<user_id>/perfiles', methods=['GET'])
def obtener_perfiles(user_id):  # noqa: E501    
    perfiles_db = PerfilDB.query.filter_by(user_id=user_id).all()
    perfiles = [perfil.to_api_model() for perfil in perfiles_db]

    if perfiles is None:
        return jsonify({"message": "No hay perfiles disponibles", "status": "error"}), 404
    else:
        return jsonify([perfil.serialize() for perfil in perfiles]), 200    
    
