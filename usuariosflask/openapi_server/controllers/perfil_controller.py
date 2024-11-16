# Se importa el fichero de configuración de los microservicios
import os, sys, requests
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(app_path)

from global_config import ContenidosConfig as contConf

from openapi_server import db
from flask import request, jsonify

from openapi_server.models.perfil import Perfil
from openapi_server.models.perfil_db import PerfilDB

from openapi_server.models.preferencias_contenido import PreferenciasContenido
from openapi_server.models.preferencias_contenido_db import PreferenciasContenidoDB

from openapi_server.models.genero_preferencias_db import GeneroPreferenciasDB
from openapi_server.models.genero_db import GeneroDB

# from openapi_server.models.historial_perfil import HistorialPerfil
from openapi_server.models.historial_perfil_db import HistorialPerfilDB

# from openapi_server.models.lista_perfil import ListaPerfil
from openapi_server.models.lista_perfil_db import ListaPerfilDB

from openapi_server.models.preferencias_contenido import PreferenciasContenido
from openapi_server.models.preferencias_contenido_db import PreferenciasContenidoDB

from openapi_server import app

@app.route('/usuario/<user_id>/perfiles/<profile_id>', methods=['PUT'])
def actualizar_perfil_usuario(user_id, profile_id):  
    """Actualiza el perfil especificado

    Actualiza el perfil especificado de un usuario # noqa: E501

    :param user_id: ID del usuario especificado
    :type user_id: int
    :param profile_id: ID del perfil a obtener
    :type profile_id: int

    :rtype: Union[Perfil, Tuple[Perfil, int], Tuple[Perfil, int, Dict[str, str]]
    """

    # Verifica si la solicitud contiene JSON
    if request.is_json:
        # Carga los datos JSON enviados en la solicitud
        perfil_data = request.get_json()
        
        # Convierte el JSON en un objeto `Perfil`
        perfil_api = Perfil.from_dict(perfil_data)
        
        # Busca el perfil en la base de datos
        perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
        
        if perfil_db is not None:
            # Actualiza los campos del perfil
            perfil_db.nombre = perfil_api.nombre
            perfil_db.foto_perfil = perfil_api.foto_perfil
            # Guarda los cambios en la base de datos
            db.session.commit()

            # Ahora hay que gestionar las preferencias de contenido
            preferencias_db = PreferenciasContenidoDB.query.filter_by(perfil_id=perfil_db.perfil_id).first()

            # Si no hay preferencias de contenido, se crean
            if preferencias_db is None:
                preferencias_db = PreferenciasContenidoDB(perfil_id=perfil_db.perfil_id)
                db.session.add(preferencias_db)
            else:
                # Actualiza las preferencias de contenido
                preferencias_db.subtitulos = perfil_api.preferencias_contenido.subtitulos
                preferencias_db.idioma_audio = perfil_api.preferencias_contenido.idioma_audio

                # Elimina los géneros anteriores
                GeneroPreferenciasDB.query.filter_by(preferencias_id=preferencias_db.preferencias_id).delete()

                # Añade los nuevos géneros
                ## Primero hay que obtener los géneros de la base de datos
                genero_preferencias_db = GeneroPreferenciasDB.query.filter_by(preferencias_id=preferencias_db.preferencias_id).all()
                for gpdb in genero_preferencias_db:
                    db.session.delete(gpdb)

                for nombre_genero in perfil_api.preferencias_contenido.generos:
                    genero = GeneroDB.query.filter_by(nombre=nombre_genero).first()
                    if genero is not None:
                        gpdb = GeneroPreferenciasDB(preferencias_id=preferencias_db.preferencias_id, genero_id=genero.genero_id)
                        db.session.add(gpdb)

            # Guarda los cambios en la base de datos
            db.session.commit()

            # Devuelve el perfil actualizado
            return jsonify(perfil_api.serialize()), 200
        else:
            return jsonify({"message": "No se ha podido actualizar el perfil", "status": "error"}), 404
    
    # Respuesta en caso de que no se envíe JSON en la solicitud
    return jsonify({"message": "La solicitud debe contener datos JSON"}), 400

@app.route('/usuario/<user_id>/perfiles/<profile_id>', methods=['DELETE'])
def borrar_perfil_usuario(user_id, profile_id):  # noqa: E501
    """Borra el perfil especificado

    Borra el perfil especificado de un usuario # noqa: E501

    :param user_id: ID del usuario específicado
    :type user_id: int
    :param profile_id: ID del perfil a obtener
    :type profile_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is not None:
        db.session.delete(perfil_db)
        db.session.commit()
        return jsonify({"message": "Perfil eliminado con éxito", "status": "success"}), 200
    else:
        return jsonify({"message": "No se ha podido eliminar el perfil", "status": "error"}), 404


@app.route('/usuario/<user_id>/perfiles', methods=['POST'])
def crear_perfil(user_id):  # noqa: E501
    """Añade un nuevo perfil al usuario especificado

    Crea un nuevo perfil para el usuario # noqa: E501

    :param user_id: ID del usuario a eliminar
    :type user_id: int
    :param perfil: Objeto del perfil a crear
    :type perfil: dict | bytes

    :rtype: Union[Perfil, Tuple[Perfil, int], Tuple[Perfil, int, Dict[str, str]]
    """

    if request.is_json:
        print(request.get_json())
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

        generos_name_list = preferencias_api.generos
        generos_db = [GeneroDB.query.filter_by(nombre=nombre).first() for nombre in generos_name_list]

        if not None in generos_db:
            for genero in generos_db:
                genero_preferencias_db = GeneroPreferenciasDB(preferencias_id=preferencias_db.preferencias_id, genero_id=genero.genero_id)
                db.session.add(genero_preferencias_db)
            db.session.commit()

        return jsonify(perfil_api.serialize()), 201
    else:
        return jsonify({"message": "Ha habido un error con su solicitud, inténtelo de nuevo más tarde", "status": "error"}), 404
 
@app.route('/usuario/<user_id>/perfiles/<profile_id>/historial', methods=['GET'])
def obtener_historial_perfil(user_id, profile_id):  # noqa: E501
    """Obtiene el historial de contenido completado por de un perfil

    Obtiene el historial de contenido completado por un perfil. Esta lista contendrá las series o películas terminadas de ver por el perfil. # noqa: E501

    :param user_id: ID del usuario específicado
    :type user_id: int
    :param profile_id: ID del perfil específico
    :type profile_id: int

    :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
    """
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404
    
    historial_db = HistorialPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id).all()
    lista_series = []
    lista_peliculas = []

    for h in historial_db:
        if (h.es_serie):
            lista_series.append(h.contenido)
        else:
            lista_peliculas.append(h.contenido)

    # Ahora se hace la petición al microservicio de contenidos para obtener los datos de las series y películas
    response_series = requests.get(f'{contConf.CONTENIDOS_BASE_URL}/obtener_lista_series', json=lista_series)

    if response_series.status_code == 200:
        series = response_series.json()
    else:
        return jsonify({"message": "No se ha podido obtener la lista de series", "status": "error"}), 404

    response_peliculas = requests.get(f'{contConf.CONTENIDOS_BASE_URL}/obtener_lista_peliculas', json=lista_peliculas)

    if response_peliculas.status_code == 200:
        peliculas = response_peliculas.json()
    else:
        return jsonify({"message": "No se ha podido obtener la lista de películas", "status": "error"}), 404
    
    print(f"\n\nSeries: {series}\n")
    print(f"\nPeliculas: {peliculas}\n")

    return jsonify({"series": series, "peliculas": peliculas}), 200

@app.route('/usuario/<user_id>/perfiles/<profile_id>/historial/<contenido_id>', methods=['POST'])
def agregar_contenido_historial(user_id, profile_id, contenido_id):
    # Buscamos el perfil en la base de datos
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404

    # Buscamos el contenido en la base de datos
    ## Hay que ver si es una serie o una película
    response_serie = requests.get(f'{contConf.CONTENIDOS_BASE_URL}/obtener_serie/{contenido_id}')
    if response_serie.status_code == 200:
        contenido_db = response_serie.json()
        es_serie = True
    else:
        response_pelicula = requests.get(f'{contConf.CONTENIDOS_BASE_URL}/obtener_pelicula/{contenido_id}')
        if response_pelicula.status_code == 200:
            contenido_db = response_pelicula.json()
            es_serie = False
        else:
            return jsonify({"message": "No se ha encontrado el contenido", "status": "error"}), 404

    # Comprobar si el contenido ya está en el historial
    historial_db = HistorialPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id, contenido=contenido_id).first()

    if historial_db is not None:
        return jsonify({"message": "El contenido ya está en el historial", "status": "error"}), 409

    # Creamos el objeto HistorialPerfilDB
    historial_db = HistorialPerfilDB(
        perfil_id=perfil_db.perfil_id,
        contenido=contenido_db['id'],
        es_serie=es_serie
    )
    db.session.add(historial_db)
    db.session.commit()

    return jsonify({"message": "Contenido añadido al historial", "status": "success"}), 201

@app.route('/usuario/<user_id>/perfiles/<profile_id>/historial/<contenido_id>', methods=['DELETE'])
def eliminar_contenido_historial(user_id, profile_id, contenido_id):
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404

    historial_db = HistorialPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id, contenido=contenido_id).first()
    if historial_db is None:
        return jsonify({"message": "No se ha encontrado el contenido en el historial", "status": "error"}), 404

    db.session.delete(historial_db)
    db.session.commit()

    return jsonify({"message": "Contenido eliminado del historial", "status": "success"}), 200

@app.route('/usuario/<user_id>/perfiles/<profile_id>/lista', methods=['GET'])
def obtener_lista_perfil(user_id, profile_id):  # noqa: E501
    """Obtiene la lista de un perfil concreto

    Obtiene la lista de contenidos guardados para ver de un perfil # noqa: E501

    :param user_id: ID del usuario específicado
    :type user_id: int
    :param profile_id: ID del perfil específico
    :type profile_id: int

    :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
    """
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404
    
    lista_perfil = ListaPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id).all()
    lista_series = []
    lista_peliculas = []

    for h in historial_db:
        if (h.es_serie):
            lista_series.append(h.contenido)
        else:
            lista_peliculas.append(h.contenido)

    contConf.CONTENIDOS_BASE_URL = "http://localhost:8081"
    # Ahora se hace la petición al microservicio de contenidos para obtener los datos de las series y películas
    response_series = requests.get(f'{contConf.CONTENIDOS_BASE_URL}/obtener_lista_series', json=lista_series)

    if response_series.status_code == 200:
        series = response_series.json()
    else:
        return jsonify({"message": "No se ha podido obtener la lista de series", "status": "error"}), 404

    response_peliculas = requests.get(f'{contConf.CONTENIDOS_BASE_URL}/obtener_lista_peliculas', json=lista_peliculas)

    if response_peliculas.status_code == 200:
        peliculas = response_peliculas.json()
    else:
        return jsonify({"message": "No se ha podido obtener la lista de películas", "status": "error"}), 404
    
    print(f"\n\nSeries: {series}\n")
    print(f"\nPeliculas: {peliculas}\n")

    return jsonify({"series": series, "peliculas": peliculas}), 200

@app.route('/usuario/<user_id>/perfiles/<profile_id>/lista/<contenido_id>', methods=['POST'])
def agregar_contenido_lista(user_id, profile_id, contenido_id):
    # Buscamos el perfil en la base de datos
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404

    # Buscamos el contenido en la base de datos
    ## Hay que ver si es una serie o una película
    serie_db = SerieDB.query.filter_by(serie_id=contenido_id).first()
    if serie_db is not None:
        es_serie = True
        contenido_db = serie_db
    else:
        pelicula_db = PeliculaDB.query.filter_by(pelicula_id=contenido_id).first()
        if pelicula_db is not None:
            es_serie = False
            contenido_db = pelicula_db
        else:
            return jsonify({"message": "No se ha encontrado el contenido", "status": "error"}), 404

    # Comprobar si el contenido ya está en el historial
    lista_db = ListaPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id, contenido=contenido_id).first()
    if lista_db is not None:
        return jsonify({"message": "El contenido ya está en la lista", "status": "error"}), 409

    # Creamos el objeto HistorialPerfilDB
    lista_db = ListaPerfilDB(perfil_id=perfil_db.perfil_id, contenido=contenido_db.contenido_id, es_serie=es_serie)
    db.session.add(lista_db)
    db.session.commit()

    return jsonify({"message": "Contenido añadido al historial", "status": "success"}), 201

@app.route('/usuario/<user_id>/perfiles/<profile_id>/lista/<contenido_id>', methods=['DELETE'])
def eliminar_contenido_lista(user_id, profile_id, contenido_id):
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is None:
        return jsonify({"message": "No se ha encontrado el perfil", "status": "error"}), 404

    lista_db = ListaPerfilDB.query.filter_by(perfil_id=perfil_db.perfil_id, contenido=contenido_id).first()
    if lista_db is None:
        return jsonify({"message": "No se ha encontrado el contenido en el historial", "status": "error"}), 404

    db.session.delete(lista_db)
    db.session.commit()

    return jsonify({"message": "Contenido eliminado del historial", "status": "success"}), 200

@app.route('/usuario/<user_id>/perfiles/<profile_id>', methods=['GET'])
def obtener_perfil_usuario(user_id, profile_id):  # noqa: E501
    """Obtiene el perfil específico de un usuario concreto

    Obtiene el perfil específico de un usuario concreto # noqa: E501

    :param user_id: ID del usuario específicado
    :type user_id: int
    :param profile_id: ID del perfil a obtener
    :type profile_id: int

    :rtype: Union[Perfil, Tuple[Perfil, int], Tuple[Perfil, int, Dict[str, str]]
    """
    
    perfil_db = PerfilDB.query.filter_by(user_id=user_id, perfil_id=profile_id).first()
    if perfil_db is not None:
        perfil = perfil_db.to_api_model()
        if perfil is None:
            return jsonify({"message": "No hay perfiles disponibles", "status": "error"}), 404
        else:
            return jsonify(perfil.serialize()), 200
    

@app.route('/usuario/<user_id>/perfiles', methods=['GET'])
def obtener_perfiles(user_id):  # noqa: E501
    """Obtiene todos los perfiles del usuario especificado

    Lista los perfiles de un usuario # noqa: E501

    :param user_id: ID del usuario a eliminar
    :type user_id: int

    :rtype: Union[List[Perfil], Tuple[List[Perfil], int], Tuple[List[Perfil], int, Dict[str, str]]
    """
    
    perfiles_db = PerfilDB.query.filter_by(user_id=user_id).all()
    perfiles = [perfil.to_api_model() for perfil in perfiles_db]

    if perfiles is None:
        return jsonify({"message": "No hay perfiles disponibles", "status": "error"}), 404
    else:
        return jsonify([perfil.serialize() for perfil in perfiles]), 200    
    
# @app.route('/usuario/<user_id>/perfiles/<profile_id>/historial', methods=['GET'])
# def obtener_historial_perfil(user_id, profile_id):
#     """Obtiene el historial de contenido completado por de un perfil

#     Obtiene el historial de contenido completado por un perfil. Esta lista contendrá las series o películas terminadas de ver por el perfil. # noqa: E501

#     :param user_id: ID del usuario específicado
#     :type user_id: int
#     :param profile_id: ID del perfil específico
#     :type profile_id: int

#     :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
#     """
#     return 'do some magic!'

# @app.route('/usuario/<user_id>/perfiles/<profile_id>/lista', methods=['GET'])
# def obtener_lista_perfil(user_id, profile_id):
#     """Obtiene la lista de un perfil concreto

#     Obtiene la lista de contenidos guardados para ver de un perfil # noqa: E501
    
#     :param user_id: ID del usuario específicado
#     :type user_id: int
#     :param profile_id: ID del perfil específico
#     :type profile_id: int
    
#     :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
#     """
    
#     return 'do some magic!'

# @app.route('/usuario/<user_id>/perfiles/<profile_id>/agregar_contenido_lista', methods=['GET'])
# def obtener_lista_perfil(user_id, profile_id):
#     """Obtiene la lista de un perfil concreto

#     Obtiene la lista de contenidos guardados para ver de un perfil # noqa: E501
    
#     :param user_id: ID del usuario específicado
#     :type user_id: int
#     :param profile_id: ID del perfil específico
#     :type profile_id: int
    
#     :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
#     """
    
#     return 'do some magic!'