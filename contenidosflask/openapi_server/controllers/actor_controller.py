from openapi_server import app

from openapi_server.models.actor import Actor  # noqa: E501
from openapi_server.models.actor_db import ActorDB
from openapi_server.models.actor_update import ActorUpdate  # noqa: E501

from openapi_server.models.pelicula_db import PeliculaDB
from openapi_server.models.serie_db import SerieDB

from flask import jsonify, request
from bson import ObjectId

@app.route('/actores/<actor_id>', methods=['PUT'])
def actualizar_actor(actor_id):  # noqa: E501
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

@app.route('/actores', methods=['POST'])
def crear_actor():  # noqa: E501
    if request.is_json:
        actor_api = Actor.from_dict(request.get_json())

    if (actor_api):
        actor_db = actor_api.to_db_model()
        actor_db.save()
        return jsonify({"message": "Actor creado con éxito", "status": "success"}), 201
    else:
        return jsonify({"message": "Error al crear el actor", "status": "error"}), 400

@app.route('/actores/<actor_id>', methods=['DELETE'])
def eliminar_actor(actor_id):  # noqa: E501
    actor = ActorDB.objects(id=ObjectId(actor_id)).first() 
    if not actor:
        return jsonify({"message": "Actor no encontrado", "status": "error"}), 404
    
    # Elimina referencias en Serie y Pelicula
    SerieDB.objects.update(pull__actores=actor)  # Remueve el actor de las listas de actores en Serie
    PeliculaDB.objects.update(pull__actores=actor)  # Remueve el actor de las listas de actores en Pelicula

    actor.delete()
    return jsonify({"message": "Actor eliminado correctamente", "status": "success"}), 200
   
@app.route('/actores', methods=['GET'])
def listar_actores():  # noqa: E501
    actores_db = ActorDB.objects()
    list_actores_api = [actor.to_api_model() for actor in actores_db]
    return jsonify(list_actores_api), 200

@app.route('/actores/<actor_id>', methods=['GET'])
def obtener_actor(actor_id):  # noqa: E501
    actor_db = ActorDB.objects.get(id=ObjectId(actor_id))
    if not actor_db:
        return jsonify({"message": "Actor no encontrado", "status": "error"}), 404

    return jsonify(actor_db.to_api_model()), 200
