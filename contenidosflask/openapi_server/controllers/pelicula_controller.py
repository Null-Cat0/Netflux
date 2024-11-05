from openapi_server.models.actor import Actor  # noqa: E501
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


def actualizar_pelicula(pelicula_id, pelicula_update):  # noqa: E501
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
    return 'do some magic!'


def asignar_actor_a_pelicula(pelicula_id, asignar_actor_a_serie_request):  # noqa: E501
    """Asignar un actor a una película

    Asigna un actor existente a una película específica. # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int
    :param asignar_actor_a_serie_request: ID del actor a asignar
    :type asignar_actor_a_serie_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if request.is_json:
        asignar_actor_a_serie_request = AsignarActorASerieRequest.from_dict(request.get_json())  # noqa: E501
    return 'do some magic!'

@app.route('/crear_pelicula', methods=['POST'])
def crear_pelicula():  # noqa: E501
    """Crear una nueva película

    Crea una nueva película con la información proporcionada. # noqa: E501

    :param pelicula: Objeto de la película a crear
    :type pelicula: dict | bytes

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    if request.is_json:
        titulo = request.json.get('titulo')
        genero = request.json.get('genero')
        sinopsis = request.json.get('sinopsis')
        anio_estreno = request.json.get('anio_estreno')
        duracion = request.json.get('duracion')
        actores = [ObjectId(id) for id in request.json.get('actores')]
        pelicula_api = Pelicula(titulo=titulo, genero=genero, sinopsis=sinopsis, anio_estreno=anio_estreno, duracion=duracion, actores=actores)
        pelicula_db = pelicula_api.to_db_model()
        pelicula_db.save()
        return jsonify({"message": "Película creada con éxito", "status": "success"}), 201


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
    pelicula_db.actores.remove(ObjectId(actor_id))
    pelicula_db.save()
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
    pelicula_db.delete()
    return jsonify({"message": "Película eliminada con éxito", "status": "success"}), 200

@app.route('/listar_actores_de_pelicula/<pelicula_id>', methods=['GET'])
def listar_actores_de_pelicula(pelicula_id):  # noqa: E501
    """Listar actores de una película específica

    Obtiene una lista de todos los actores que participan en una película específica. # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int

    :rtype: Union[List[Actor], Tuple[List[Actor], int], Tuple[List[Actor], int, Dict[str, str]]
    """

    pelicula_db = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    pelicula_api = pelicula_db.to_api_model()
    actores_json = [actor.serialize() for actor in pelicula_api.actores]
    return jsonify(actores_json)
    

@app.route('/listar_peliculas', methods=['GET'])
def listar_peliculas():  # noqa: E501
    """Listar todas las películas

    Obtiene una lista de todas las películas disponibles en el sistema, incluyendo información básica como el título, género y año de estreno. # noqa: E501


    :rtype: Union[List[Pelicula], Tuple[List[Pelicula], int], Tuple[List[Pelicula], int, Dict[str, str]]
    """
    peliculas_db = PeliculaDB.objects()
    return [pelicula.to_api_model() for pelicula in peliculas_db]

@app.route('/pelicula/<pelicula_id>', methods=['GET'])
def obtener_pelicula(pelicula_id):  # noqa: E501
    """Obtener una película específica

    Obtiene la información detallada de una película específica por su ID. # noqa: E501

    :param pelicula_id: ID de la película a obtener
    :type pelicula_id: int

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    pelicula_db = PeliculaDB.objects.get(id=ObjectId(pelicula_id))
    return jsonify(pelicula_db.to_api_model())
    


def obtener_precuela_pelicula(pelicula_id):  # noqa: E501
    """Obtiene la precuela de una película específica

    Obtiene la precuela de una película específica # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_secuela_pelicula(pelicula_id):  # noqa: E501
    """Obtiene la secuela de una película específica

    Obtiene la secuela de una película específica # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    return 'do some magic!'
