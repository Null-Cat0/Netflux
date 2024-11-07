from openapi_server.models.actor import Actor  # noqa: E501
from openapi_server.models.actor_db import ActorDB  # noqa: E501
from openapi_server.models.asignar_actor_a_serie_request import AsignarActorASerieRequest  # noqa: E501
from openapi_server.models.pelicula import Pelicula  # noqa: E501
from openapi_server.models.pelicula_update import PeliculaUpdate  # noqa: E501
from openapi_server import util
from openapi_server import db
from flask import request
from openapi_server import app
from flask import jsonify
from bson import ObjectId
from openapi_server.models.pelicula_db import PeliculaDB

@app.route('/actualizar_pelicula/<pelicula_id>', methods=['PUT'])
def actualizar_pelicula(pelicula_id):  # noqa: E501
    """Actualizar una película existente

    Actualiza la información de una película específica por su ID. # noqa: E501

    :param pelicula_id: ID de la película a actualizar
    :type pelicula_id: int
    :param pelicula_update: Objeto de la película con la información actualizada
    :type pelicula_update: dict | bytes

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    if request.is_json:
        pelicula_update = PeliculaUpdate.from_dict(request.get_json())  # noqa: E501

    pelicula_to_update = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    if not pelicula_to_update:
        return jsonify({"message": "Película no encontrada", "status": "error"}), 404
    
    pelicula_db = pelicula_update.to_db_model()
    pelicula_to_update.titulo = pelicula_db.titulo
    pelicula_to_update.genero = pelicula_db.genero
    pelicula_to_update.sinopsis = pelicula_db.sinopsis
    pelicula_to_update.anio_estreno = pelicula_db.anio_estreno
    pelicula_to_update.duracion = pelicula_db.duracion

    # Reemplazar los actores
    actores_db = [ActorDB.objects.get(id=ObjectId(id)) for id in pelicula_update.actores]
    pelicula_to_update.actores = actores_db # Se cambia la lista de actores por la nueva

    # Reemplazar la secuela y precuela
    if pelicula_update.secuela:
        pelicula_to_update.secuela = PeliculaDB.objects.get(id=ObjectId(pelicula_update.secuela))
    
    if pelicula_update.precuela:
        pelicula_to_update.precuela = PeliculaDB.objects.get(id=ObjectId(pelicula_update.precuela))

    pelicula_to_update.save()
    return jsonify({"message": "Película actualizada correctamente", "status": "success"}), 200

@app.route('/asignar_actor_pelicula/<pelicula_id>', methods=['POST'])
def asignar_actor_a_pelicula(pelicula_id):  # noqa: E501
    """Asignar un actor a una película

    Asigna un actor existente a una película específica. # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int
    :param asignar_actor_a_serie_request: ID del actor a asignar
    :type asignar_actor_a_serie_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    
    if request.is_json:
        actor_a_asignar = AsignarActorASerieRequest.from_dict(request.get_json())

    pelicula_db = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    if not pelicula_db:
        return jsonify({"message": "Película no encontrada", "status": "error"}), 404

    if not ActorDB.objects.get(id=ObjectId(actor_a_asignar.actor_id)):
        return jsonify({"message": "Actor no encontrado", "status": "error"}), 404

    pelicula_db.update(add_to_set__actores=actor_a_asignar.actor_id)
    return jsonify({"message": "Actor asignado con éxito", "status": "success"}), 200

@app.route('/crear_pelicula', methods=['POST'])
def crear_pelicula():  # noqa: E501
    """Crear una nueva película

    Crea una nueva película con la información proporcionada. # noqa: E501

    :param pelicula: Objeto de la película a crear
    :type pelicula: dict | bytes

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    if request.is_json:
        pelicula_api = Pelicula.from_dict(request.get_json())

    if (pelicula_api):
        pelicula_db = pelicula_api.to_db_model()
        pelicula_db.save()
        return jsonify({"message": "Película creada con éxito", "status": "success"}), 201
    else:
        return jsonify({"message": "Error al crear la película", "status": "error"}), 400


@app.route('/eliminar_actor_pelicula/<pelicula_id>/<actor_id>', methods=['DELETE'])
def eliminar_actor_pelicula(pelicula_id, actor_id):  # noqa: E501
    """Elimnar un actor de una película

    Elimina un actor existente de una película específica. # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int
    :param actor_id: ID del actor
    :type actor_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    pelicula_db = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    if not pelicula_db:
        return jsonify({"message": "Película no encontrada", "status": "error"}), 404 

    actor_db = ActorDB.objects.get(id=ObjectId(actor_id))
    if not actor_db in pelicula_db.actores:
        return jsonify({"message": "Actor no encontrado en la película", "status": "error"}), 404

    pelicula_db.update(pull__actores=actor_db)
    return jsonify({"message": "Actor eliminado con éxito", "status": "success"}), 200


@app.route('/eliminar_pelicula/<pelicula_id>', methods=['DELETE'])
def eliminar_pelicula(pelicula_id):  # noqa: E501
    """Eliminar una película

    Elimina una película específica por su ID. # noqa: E501

    :param pelicula_id: ID de la película a eliminar
    :type pelicula_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """

    pelicula_db = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    if not pelicula_db:
        return jsonify({"message": "Película no encontrada", "status": "error"}), 404

    pelicula_db.delete()
    return jsonify({"message": "Película eliminada con éxito", "status": "success"}), 200

@app.route('/listar_actores_pelicula/<pelicula_id>', methods=['GET'])
def listar_actores_de_pelicula(pelicula_id):  # noqa: E501
    """Listar actores de una película específica

    Obtiene una lista de todos los actores que participan en una película específica. # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int

    :rtype: Union[List[Actor], Tuple[List[Actor], int], Tuple[List[Actor], int, Dict[str, str]]
    """

    pelicula_db = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    if not pelicula_db:
        return jsonify({"message": "Película no encontrada", "status": "error"}), 404

    pelicula_api = pelicula_db.to_api_model()
    actores_json = [actor for actor in pelicula_api.actores]
    return jsonify(actores_json), 200
    

@app.route('/listar_peliculas', methods=['GET'])
def listar_peliculas():  # noqa: E501
    """Listar todas las películas

    Obtiene una lista de todas las películas disponibles en el sistema, incluyendo información básica como el título, género y año de estreno. # noqa: E501


    :rtype: Union[List[Pelicula], Tuple[List[Pelicula], int], Tuple[List[Pelicula], int, Dict[str, str]]
    """
    peliculas_db = PeliculaDB.objects()
    list_peliculas = [pelicula.to_api_model() for pelicula in peliculas_db]
    return jsonify(list_peliculas), 200

@app.route('/obtener_pelicula/<pelicula_id>', methods=['GET'])
def obtener_pelicula(pelicula_id):  # noqa: E501
    """Obtener una película específica

    Obtiene la información detallada de una película específica por su ID. # noqa: E501

    :param pelicula_id: ID de la película a obtener
    :type pelicula_id: int

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    pelicula_db = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    if not pelicula_db:
        return jsonify({"message": "Película no encontrada", "status": "error"}), 404
    
    return jsonify(pelicula_db.to_api_model()), 200
    
@app.route('/obtener_precuela_pelicula/<pelicula_id>', methods=['GET'])
def obtener_precuela_pelicula(pelicula_id):  # noqa: E501
    """Obtiene la precuela de una película específica

    Obtiene la precuela de una película específica # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """

    pelicula_db = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    if not pelicula_db:
        return jsonify({"message": "Película no encontrada", "status": "error"}), 404

    return jsonify(pelicula_db.precuela), 200

@app.route('/obtener_secuela_pelicula/<pelicula_id>', methods=['GET'])
def obtener_secuela_pelicula(pelicula_id):  # noqa: E501
    """Obtiene la secuela de una película específica

    Obtiene la secuela de una película específica # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """

    pelicula_db = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    if not pelicula_db:
        return jsonify({"message": "Película no encontrada", "status": "error"}), 404

    return jsonify(pelicula_db.secuela), 200
