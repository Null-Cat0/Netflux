from openapi_server.models.actor_update import ActorUpdate  # noqa: E501
from openapi_server.models.actor import Actor  # noqa: E501
from openapi_server.models.actor_db import ActorDB
from openapi_server.models.pelicula_db import PeliculaDB
from openapi_server.models.serie_db import SerieDB
from openapi_server import db
from flask import request
from openapi_server import app
from flask import jsonify
from bson import ObjectId

def actualizar_actor(actor_id, actor_update):  # noqa: E501
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
    return 'do some magic!'

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
        actor_db = actor_api.to_db_model()
        actor_db.save()
        return jsonify({"message": "Actor creado con éxito", "status": "success"}), 201

@app.route('/eliminar_actor/<actor_id>', methods=['DELETE'])
def eliminar_actor(actor_id):  # noqa: E501
    """Eliminar un actor

    Elimina un actor específico por su ID. # noqa: E501

    :param actor_id: ID del actor a eliminar
    :type actor_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    actor = Actor.objects(id=ObjectId(actor_id)).first()
    if not actor:
        return jsonify({"message": "Actor no encontrado", "status": "fail"}), 404
    
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
    return [actor.to_api_model() for actor in actores_db]


def listar_peliculas_de_actor(actor_id):  # noqa: E501
    """Listar películas en las que ha participado un actor en específico.

    Obtiene una lista de todas las películas en las que ha participado un actor. # noqa: E501

    :param actor_id: ID del actor
    :type actor_id: int

    :rtype: Union[List[Pelicula], Tuple[List[Pelicula], int], Tuple[List[Pelicula], int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_series_de_actor(actor_id):  # noqa: E501
    """Listar series en las que ha participado un actor en específico.

    Obtiene una lista de todas las series en las que ha participado un actor. # noqa: E501

    :param actor_id: ID del actor
    :type actor_id: int

    :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
    """
    return 'do some magic!'

@app.route('/actor/<actor_id>', methods=['GET'])
def obtener_actor(actor_id):  # noqa: E501
    """Obtener un actor específico

    Obtiene la información detallada de un actor específico por su ID. # noqa: E501

    :param actor_id: ID del actor a obtener
    :type actor_id: int

    :rtype: Union[Actor, Tuple[Actor, int], Tuple[Actor, int, Dict[str, str]]
    """ 

    actor_db = ActorDB.objects.get(id=ObjectId(actor_id))
    actor_api = actor_db.to_api_model()
    return jsonify(actor_api)