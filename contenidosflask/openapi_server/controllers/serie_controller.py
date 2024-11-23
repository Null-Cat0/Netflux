from openapi_server import app

from openapi_server.models.actor_db import ActorDB  # noqa: E501
from openapi_server.models.genero_db import GeneroDB 
from openapi_server.models.asignar_actor_request import AsignarActorRequest  # noqa: E501

from openapi_server.models.serie import Serie  # noqa: E501
from openapi_server.models.serie_db import SerieDB
from openapi_server.models.serie_update import SerieUpdate  # noqa: E501

from flask import jsonify, request
from bson import ObjectId

@app.route('/actualizar_serie/<serie_id>', methods=['PUT'])
def actualizar_serie(serie_id):  # noqa: E501
    """Actualizar una serie existente

    Actualiza la información de una serie específica por su ID. # noqa: E501

    :param serie_id: ID de la serie a actualizar
    :type serie_id: int
    :param serie_update: Objeto de la serie con la información actualizada
    :type serie_update: dict | bytes

    :rtype: Union[Serie, Tuple[Serie, int], Tuple[Serie, int, Dict[str, str]]
    """
    if request.is_json:
        serie_update = SerieUpdate.from_dict(request.get_json())
 
    serie_to_update = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie_to_update:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404
    
    serie_db = serie_update.to_db_model()

    if serie_db.genero == []:
        return jsonify({"message": "La serie debe tener al menos un género", "status": "error"}), 400
    
    if serie_db.titulo:
        serie_to_update.titulo = serie_db.titulo
    if serie_db.genero :
        serie_to_update.genero = serie_db.genero

    if serie_db.sinopsis:
        serie_to_update.sinopsis = serie_db.sinopsis
    if serie_db.anio_estreno:
        serie_to_update.anio_estreno = serie_db.anio_estreno

    if serie_db.temporadas:
        serie_to_update.temporadas = serie_db.temporadas

    # Reemplazar los generos
    if serie_db.genero:
        generos_db = [GeneroDB.objects.get(id=ObjectId(id)) for id in serie_update.genero]
        serie_to_update.genero = generos_db # Se cambia la lista de generos por la nueva

    # Reemplazar los actores
    if serie_db.actores:
        actores_db = [ActorDB.objects.get(id=ObjectId(id)) for id in serie_update.actores]
        serie_to_update.actores = actores_db # Se cambia la lista de actores por la nueva
    elif serie_db.actores == []:
        serie_to_update.actores = []
    serie_to_update.save()
    return jsonify({"message": "Serie actualizada correctamente", "status": "success"}), 200

@app.route('/asignar_actor_serie/<serie_id>', methods=['POST'])
def asignar_actor_a_serie(serie_id): # noqa: E501
    """Asignar un actor a una serie

    Asigna un actor existente a una serie específica. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param asignar_actor_a_serie_request: ID del actor a asignar
    :type asignar_actor_a_serie_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if request.is_json:
        actor_a_asignar = AsignarActorRequest.from_dict(request.get_json())  # noqa: E501
    
    serie_db = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie_db:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404
    
    if not ActorDB.objects.get(id=ObjectId(actor_a_asignar.actor_id)):
        return jsonify({"message": "Actor no encontrado", "status": "error"}), 404

    serie_db.update(add_to_set__actores=ObjectId(actor_a_asignar.actor_id))
    return jsonify({"message": "Actor asignado a la serie", "status": "success"}), 200

@app.route('/crear_serie', methods=['POST'])
def crear_serie():  # noqa: E501
    """Crear una nueva serie

    Crea una nueva serie de televisión con la información proporcionada. # noqa: E501

    :param serie: Objeto de la serie a crear
    :type serie: dict | bytes

    :rtype: Union[Serie, Tuple[Serie, int], Tuple[Serie, int, Dict[str, str]]
    """
    if request.is_json:
        serie_api = Serie.from_dict(request.get_json())

    if serie_api:
        if not serie_api.genero or not isinstance(serie_api.genero, list):
            return jsonify({"message": "Error: El campo 'genero' es obligatorio y debe contener al menos un género.", "status": "error"}), 400
        
        from openapi_server.models.genero_db import GeneroDB
        generos_invalidos = [g for g in serie_api.genero if not GeneroDB.objects(id=g).first()]
        if generos_invalidos:
            return jsonify({
                "message": f"Error: Los siguientes géneros no son válidos o no existen: {generos_invalidos}",
                "status": "error"
            }), 400
        
        serie_db = serie_api.to_db_model()
        serie_db.save()
        return jsonify({"message": "Serie creada con éxito", "status": "success"}), 201
    else:
        return jsonify({"message": "Error al crear la serie", "status": "error"}), 400

@app.route('/eliminar_actor_serie/<serie_id>/<actor_id>', methods=['DELETE'])
def eliminar_actor_serie(serie_id, actor_id):  # noqa: E501
    """Elimnar un actor de una serie

    Elimina un actor existente de una serie específica. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param actor_id: ID del actor
    :type actor_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    serie_db = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie_db:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    actor_db = ActorDB.objects.get(id=ObjectId(actor_id))
    if not actor_db in serie_db.actores:
        return jsonify({"message": "Actor no encontrado en la serie", "status": "error"}), 404
    
    serie_db.update(pull__actores=actor_db)
    return jsonify({"message": "Actor eliminado de la serie", "status": "success"}), 200

@app.route('/eliminar_serie/<serie_id>', methods=['DELETE'])
def eliminar_serie(serie_id):  # noqa: E501
    """Eliminar una serie

    Elimina una serie específica por su ID. # noqa: E501

    :param serie_id: ID de la serie a eliminar
    :type serie_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    serie_db = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie_db:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    serie_db.delete()
    return jsonify({"message": "Serie eliminada correctamente", "status": "success"}), 200

@app.route('/listar_actores_serie/<serie_id>', methods=['GET'])
def listar_actores_de_serie(serie_id):  # noqa: E501
    """Listar los actores de una serie específica

    Obtiene una lista de todos los actores que participan en una serie específica. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int

    :rtype: Union[List[Actor], Tuple[List[Actor], int], Tuple[List[Actor], int, Dict[str, str]]
    """
    serie_db = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie_db:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    actores = serie_db.actores
    actores_api = [actor.to_api_model() for actor in actores]
    return jsonify(actores_api), 200

@app.route('/listar_series', methods=['GET'])
def listar_series():  # noqa: E501
    """Listar todas las series

    Obtiene una lista de todas las series de televisión disponibles en el sistema, incluyendo información básica como el título, género y año de estreno. # noqa: E501

    :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
    """
    series_db = SerieDB.objects()
    list_series_api = [serie.to_api_model() for serie in series_db]
    return jsonify(list_series_api), 200

@app.route('/obtener_serie/<serie_id>', methods=['GET'])
def obtener_serie(serie_id):  # noqa: E501
    """Obtener una serie específica

    Obtiene la información detallada de una serie específica por su ID. # noqa: E501

    :param serie_id: ID de la serie a obtener
    :type serie_id: int

    :rtype: Union[Serie, Tuple[Serie, int], Tuple[Serie, int, Dict[str, str]]
    """
    serie_db = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie_db:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    return jsonify(serie_db.to_api_model()), 200

@app.route('/obtener_lista_series', methods=['GET'])
def obtener_lista_series():
    if request.is_json:
        lista_ids = request.get_json()
    else:
        return jsonify({"message": "Error al obtener la lista de series", "status": "error"}), 400

    series_db = SerieDB.objects(id__in=lista_ids)
    list_series_api = [serie.to_api_model() for serie in series_db]
    return jsonify(list_series_api), 200
