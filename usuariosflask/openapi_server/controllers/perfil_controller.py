from openapi_server.models.perfil import Perfil  # noqa: E501

from openapi_server import db

from flask import request, jsonify

from openapi_server.models.perfil import Perfil
from openapi_server.models.perfil_db import PerfilDB

from openapi_server.models.preferencias_contenido import PreferenciasContenido
from openapi_server.models.preferencias_contenido_db import PreferenciasContenidoDB

from openapi_server.models.genero_preferencias_db import GeneroPreferenciasDB
from openapi_server.models.genero_db import GeneroDB

from openapi_server.models.preferencias_contenido import PreferenciasContenido
from openapi_server.models.preferencias_contenido_db import PreferenciasContenidoDB

from openapi_server.models.genero_preferencias_db import GeneroPreferenciasDB

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
 
def obtener_historial_perfil(user_id, profile_id):  # noqa: E501
    """Obtiene el historial de contenido completado por de un perfil

    Obtiene el historial de contenido completado por un perfil. Esta lista contendrá las series o películas terminadas de ver por el perfil. # noqa: E501

    :param user_id: ID del usuario específicado
    :type user_id: int
    :param profile_id: ID del perfil específico
    :type profile_id: int

    :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_lista_perfil(user_id, profile_id):  # noqa: E501
    """Obtiene la lista de un perfil concreto

    Obtiene la lista de contenidos guardados para ver de un perfil # noqa: E501

    :param user_id: ID del usuario específicado
    :type user_id: int
    :param profile_id: ID del perfil específico
    :type profile_id: int

    :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
    """
    return 'do some magic!'

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