from openapi_server import app

from openapi_server.models.actor import Actor  # noqa: E501
from openapi_server.models.actor_db import ActorDB
from openapi_server.models.actor_update import ActorUpdate  # noqa: E501

from openapi_server.models.pelicula_db import PeliculaDB
from openapi_server.models.serie_db import SerieDB

from flask import jsonify, request
from bson import ObjectId

@app.route('/actualizar_actor/<actor_id>', methods=['PUT'])
def actualizar_actor(actor_id):  # noqa: E501
    """Actualizar un actor existente

    Actualiza la información de un actor específico por su ID. # noqa: E501

    :param actor_id: ID del actor a actualizar
    :type actor_id: int
    :param actor_update: Objeto del actor con la información actualizada
    :type actor_update: dict | bytes

    :rtype: Union[Actor, Tuple[Actor, int], Tuple[Actor, int, Dict[str, str]]
    """
    if request.is_json:
        actor_update = ActorUpdate.from_dict(request.get_json())  # noqa: E501

    actor_to_update = ActorDB.objects.get(id=ObjectId(actor_id))
    if not actor_to_update:
        return jsonify({"message": "Actor no encontrado", "status": "error"}), 404

    actor_db = actor_update.to_db_model()

    if actor_db.nombre:
        actor_to_update.nombre = actor_db.nombre
    if actor_db.fecha_nacimiento:
        actor_to_update.fecha_nacimiento = actor_db.fecha_nacimiento
    if actor_db.nacionalidad:
        actor_to_update.nacionalidad = actor_db.nacionalidad
    if actor_db.biografia:
        actor_to_update.biografia = actor_db.biografia

    actor_to_update.save()
    return jsonify({"message": "Actor actualizado correctamente", "status": "success"}), 200

@app.route('/crear_actor', methods=['POST'])
def crear_actor():  # noqa: E501
    """Crear un nuevo actor

    Crea un nuevo actor con la información proporcionada. # noqa: E501

    :param actor: Objeto del actor a crear
    :type actor: dict | bytes

    :rtype: Union[Actor, Tuple[Actor, int], Tuple[Actor, int, Dict[str, str]]
    """
    if request.is_json:
        actor_api = Actor.from_dict(request.get_json())

    if (actor_api):
        actor_db = actor_api.to_db_model()
        actor_db.save()
        return jsonify({"message": "Actor creado con éxito", "status": "success"}), 201
    else:
        return jsonify({"message": "Error al crear el actor", "status": "error"}), 400

@app.route('/eliminar_actor/<actor_id>', methods=['DELETE'])
def eliminar_actor(actor_id):  # noqa: E501
    """Eliminar un actor

    Elimina un actor específico por su ID. # noqa: E501

    :param actor_id: ID del actor a eliminar
    :type actor_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    actor = ActorDB.objects(id=ObjectId(actor_id)).first()
    if not actor:
        return jsonify({"message": "Actor no encontrado", "status": "error"}), 404
    
    # Elimina referencias en Serie y Pelicula
    SerieDB.objects.update(pull__actores=actor)  # Remueve el actor de las listas de actores en Serie
    PeliculaDB.objects.update(pull__actores=actor)  # Remueve el actor de las listas de actores en Pelicula

    actor.delete()
    return jsonify({"message": "Actor eliminado correctamente", "status": "success"}), 200
   
@app.route('/listar_actores', methods=['GET'])
def listar_actores():  # noqa: E501
    """Listar todos los actores

    Obtiene una lista de todos los actores registrados en el sistema. # noqa: E501

    :rtype: Union[List[Actor], Tuple[List[Actor], int], Tuple[List[Actor], int, Dict[str, str]]
    """
    actores_db = ActorDB.objects()
    list_actores_api = [actor.to_api_model() for actor in actores_db]
    return jsonify(list_actores_api), 200

# @app.route('/listar_peliculas_actor/<actor_id>', methods=['GET'])
# def listar_peliculas_de_actor(actor_id):  # noqa: E501
#     """Listar películas en las que ha participado un actor en específico.

#     Obtiene una lista de todas las películas en las que ha participado un actor. # noqa: E501

#     :param actor_id: ID del actor
#     :type actor_id: int

#     :rtype: Union[List[Pelicula], Tuple[List[Pelicula], int], Tuple[List[Pelicula], int, Dict[str, str]]
#     """

#     actor_db = ActorDB.objects.get(id=ObjectId(actor_id))
#     if not actor_db:
#         return jsonify({"message": "Actor no encontrado", "status": "error"}), 404

#     peliculas = PeliculaDB.objects(actores=actor_db)
#     peliculas_api = [pelicula.to_api_model() for pelicula in peliculas]
#     return jsonify(peliculas_api), 200

# @app.route('/listar_series_actor/<actor_id>', methods=['GET'])
# def listar_series_de_actor(actor_id):  # noqa: E501
#     """Listar series en las que ha participado un actor en específico.

#     Obtiene una lista de todas las series en las que ha participado un actor. # noqa: E501

#     :param actor_id: ID del actor
#     :type actor_id: int

#     :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
#     """

#     actor_db = ActorDB.objects.get(id=ObjectId(actor_id))
#     if not actor_db:
#         return jsonify({"message": "Actor no encontrado", "status": "error"}), 404

#     series = SerieDB.objects(actores=actor_db)
#     series_api = [serie.to_api_model() for serie in series]
#     return jsonify(series_api), 200

@app.route('/obtener_actor/<actor_id>', methods=['GET'])
def obtener_actor(actor_id):  # noqa: E501
    """Obtener un actor específico

    Obtiene la información detallada de un actor específico por su ID. # noqa: E501

    :param actor_id: ID del actor a obtener
    :type actor_id: int

    :rtype: Union[Actor, Tuple[Actor, int], Tuple[Actor, int, Dict[str, str]]
    """ 

    actor_db = ActorDB.objects.get(id=ObjectId(actor_id))
    if not actor_db:
        return jsonify({"message": "Actor no encontrado", "status": "error"}), 404

    return jsonify(actor_db.to_api_model()), 200
