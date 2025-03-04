from openapi_server import app

from openapi_server.models.actor_db import ActorDB  # noqa: E501
from openapi_server.models.genero_db import GeneroDB 

from openapi_server.models.asignar_actor_request import AsignarActorRequest  # noqa: E501

from openapi_server.models.pelicula import Pelicula  # noqa: E501
from openapi_server.models.pelicula_db import PeliculaDB
from openapi_server.models.pelicula_update import PeliculaUpdate  # noqa: E501

from flask import jsonify, request
from bson import ObjectId

@app.route('/peliculas/<pelicula_id>', methods=['PUT'])
def actualizar_pelicula(pelicula_id):  # noqa: E501
    if request.is_json:
        pelicula_update = PeliculaUpdate.from_dict(request.get_json())  # noqa: E501

    pelicula_to_update = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    if not pelicula_to_update:
        return jsonify({"message": "Película no encontrada", "status": "error"}), 404
    
    pelicula_db = pelicula_update.to_db_model()
    if pelicula_db.titulo:
        pelicula_to_update.titulo = pelicula_db.titulo
    if pelicula_db.genero:
        pelicula_to_update.genero = pelicula_db.genero
    if pelicula_db.sinopsis:
        pelicula_to_update.sinopsis = pelicula_db.sinopsis
    if pelicula_db.anio_estreno:
        pelicula_to_update.anio_estreno = pelicula_db.anio_estreno
    if pelicula_db.duracion:
        pelicula_to_update.duracion = pelicula_db.duracion

    # Reemplazar los generos
    if pelicula_db.genero:
        generos_db = [GeneroDB.objects.get(id=ObjectId(id)) for id in pelicula_update.genero]
        pelicula_to_update.genero = generos_db

    # Reemplazar los actores
    if pelicula_db.actores:
        actores_db = [ActorDB.objects.get(id=ObjectId(id)) for id in pelicula_update.actores]
        pelicula_to_update.actores = actores_db # Se cambia la lista de actores por la nueva

    pelicula_to_update.save()
    return jsonify({"message": "Película actualizada correctamente", "status": "success"}), 200

@app.route('/peliculas/<pelicula_id>/actores', methods=['POST'])
def asignar_actor_a_pelicula(pelicula_id): # noqa: E501    
    if request.is_json:
        actor_a_asignar = AsignarActorRequest.from_dict(request.get_json())

    pelicula_db = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    if not pelicula_db:
        return jsonify({"message": "Película no encontrada", "status": "error"}), 404

    if not ActorDB.objects.get(id=ObjectId(actor_a_asignar.actor_id)):
        return jsonify({"message": "Actor no encontrado", "status": "error"}), 404

    pelicula_db.update(add_to_set__actores=actor_a_asignar.actor_id)
    return jsonify({"message": "Actor asignado con éxito", "status": "success"}), 200

@app.route('/peliculas', methods=['POST'])
def crear_pelicula():  # noqa: E501
    if request.is_json:
        pelicula_api = Pelicula.from_dict(request.get_json())

    if pelicula_api:

        if not pelicula_api.genero or not isinstance(pelicula_api.genero, list):
            return jsonify({"message": "Error: El campo 'genero' es obligatorio y debe contener al menos un género.", "status": "error"}), 400
        
        from openapi_server.models.genero_db import GeneroDB
        generos_invalidos = [g for g in pelicula_api.genero if not GeneroDB.objects(id=g).first()]
        if generos_invalidos:
            return jsonify({
                "message": f"Error: Los siguientes géneros no son válidos o no existen: {generos_invalidos}",
                "status": "error"
            }), 400
        
        pelicula_db = pelicula_api.to_db_model()
        pelicula_db.save()
        return jsonify({"message": "Película creada con éxito", "status": "success"}), 201
    else:
        return jsonify({"message": "Error al crear la película", "status": "error"}), 400

@app.route('/peliculas/<pelicula_id>', methods=['DELETE'])
def eliminar_pelicula(pelicula_id):  # noqa: E501
    pelicula_db = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    if not pelicula_db:
        return jsonify({"message": "Película no encontrada", "status": "error"}), 404

    pelicula_db.delete()

    return jsonify({"message": "Película eliminada con éxito", "status": "success"}), 200

@app.route('/peliculas', methods=['GET'])
def listar_peliculas():  # noqa: E501
    peliculas_db = PeliculaDB.objects()
    list_peliculas = [pelicula.to_api_model() for pelicula in peliculas_db]
    return jsonify(list_peliculas), 200

@app.route('/peliculas/<pelicula_id>', methods=['GET'])
def obtener_pelicula(pelicula_id):  # noqa: E501
    pelicula_db = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    if not pelicula_db:
        return jsonify({"message": "Película no encontrada", "status": "error"}), 404
    
    return jsonify(pelicula_db.to_api_model()), 200

@app.route('/obtener_lista_peliculas', methods=['GET'])
def obtener_lista_peliculas():
    if request.is_json:
        lista_ids = request.get_json()
    else:
        return jsonify({"message": "Error al obtener la lista de películas", "status": "error"}), 400

    lista_peliculas = PeliculaDB.objects(id__in=lista_ids)
    list_peliculas_api = [pelicula.to_api_model() for pelicula in lista_peliculas]
    
    return jsonify(list_peliculas_api), 200