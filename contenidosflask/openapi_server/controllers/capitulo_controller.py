from openapi_server import app

from openapi_server.models.serie_db import SerieDB
from openapi_server.models.serie_db import CapituloEmbeddedDB
from openapi_server.models.serie import CapituloEmbedded  # noqa: E501

from flask import jsonify, request
from bson import ObjectId

@app.route('/series/<serie_id>/temporadas/<temporada_id>/capitulos/<capitulo_id>', methods=['PUT'])
def actualizar_capitulo(serie_id, temporada_id, capitulo_id):  # noqa: E501
    """Actualizar un capítulo existente

    Actualiza la información de un capítulo específico de una temporada de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int
    :param capitulo_id: ID del capítulo
    :type capitulo_id: int
    :param capitulo_update: Objeto del capítulo con la información actualizada
    :type capitulo_update: dict | bytes

    :rtype: Union[Capitulo, Tuple[Capitulo, int], Tuple[Capitulo, int, Dict[str, str]]
    """
    if not request.is_json:
        return jsonify({"message": "Formato de datos no válido", "status": "error"}), 400

    capitulo_update_data = CapituloEmbedded.from_dict(request.get_json())

    serie = SerieDB.objects(id=ObjectId(serie_id)).first()
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    temporada = next((temporada for temporada in serie.temporadas if temporada.temporada_id == ObjectId(temporada_id)), None)
    if not temporada:
        return jsonify({"message": "Temporada no encontrada", "status": "error"}), 404

    capitulo = next((capitulo for capitulo in temporada.capitulos if capitulo.capitulo_id == ObjectId(capitulo_id)), None)

    if not capitulo:
        return jsonify({"message": "Capítulo no encontrado", "status": "error"}), 404

    if capitulo_update_data.numero and capitulo_update_data.numero > -1:
        capitulo.numero = capitulo_update_data.numero
    if capitulo_update_data.titulo:
        capitulo.titulo = capitulo_update_data.titulo
    if capitulo_update_data.duracion:
        capitulo.duracion = capitulo_update_data.duracion
    if capitulo_update_data.sinopsis:
        capitulo.sinopsis = capitulo_update_data.sinopsis

    serie.save()
    return jsonify({"message": "Capítulo actualizado correctamente", "status": "success"}), 200

@app.route('/series/<serie_id>/temporadas/<temporada_id>/capitulos', methods=['POST'])
def crear_capitulo(serie_id, temporada_id):  # noqa: E501
    """Crear un nuevo capítulo para una temporada

    Crea un nuevo capítulo para una temporada específica de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int
    :param capitulo: Objeto del capítulo a crear
    :type capitulo: dict | bytes

    :rtype: Union[Capitulo, Tuple[Capitulo, int], Tuple[Capitulo, int, Dict[str, str]]
    """
    if not request.is_json:
        return jsonify({"message": "Formato de datos no válido", "status": "error"}), 400

    capitulo_data = CapituloEmbedded.from_dict(request.get_json())

    serie = SerieDB.objects(id=ObjectId(serie_id)).first()
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    temporada = next((temporada for temporada in serie.temporadas if temporada.temporada_id == ObjectId(temporada_id)), None)
    if not temporada:
        return jsonify({"message": "Temporada no encontrada", "status": "error"}), 404

    capitulo_db = capitulo_data.to_db_model()
    if capitulo_db.numero < 0:
        return jsonify({"message": "Número de capítulo no válido", "status": "error"}), 400

    temporada.capitulos.append(capitulo_db)
    serie.save()
    return jsonify({"message": "Capítulo creado correctamente", "status": "success"}), 201

@app.route('/series/<serie_id>/temporadas/<temporada_id>/capitulos/<capitulo_id>', methods=['DELETE'])
def eliminar_capitulo(serie_id, temporada_id, capitulo_id):  # noqa: E501
    """Eliminar un capítulo

    Elimina un capítulo específico de una temporada de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int
    :param capitulo_id: ID del capítulo
    :type capitulo_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    serie = SerieDB.objects(id=ObjectId(serie_id)).first()
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    temporada = next((temporada for temporada in serie.temporadas if temporada.temporada_id == ObjectId(temporada_id)), None)
    if not temporada:
        return jsonify({"message": "Temporada no encontrada", "status": "error"}), 404

    capitulo = next((capitulo for capitulo in temporada.capitulos if capitulo.capitulo_id == ObjectId(capitulo_id)), None)
    if not capitulo:
        return jsonify({"message": "Capítulo no encontrado", "status": "error"}), 404

    temporada.capitulos.remove(capitulo)
    serie.save()
    return jsonify({"message": "Capítulo eliminado correctamente", "status": "success"}), 200

@app.route('/series/<serie_id>/temporadas/<temporada_id>/capitulos', methods=['GET'])
def listar_capitulos(serie_id, temporada_id):  # noqa: E501
    """Listar todos los capítulos de una temporada

    Obtiene una lista de todos los capítulos de una temporada específica de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int

    :rtype: Union[List[Capitulo], Tuple[List[Capitulo], int], Tuple[List[Capitulo], int, Dict[str, str]]
    """
    serie = SerieDB.objects(id=ObjectId(serie_id)).first()
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404
    
    temporada = next((temporada for temporada in serie.temporadas if temporada.temporada_id == ObjectId(temporada_id)), None)
    if not temporada:
        return jsonify({"message": "Temporada no encontrada", "status": "error"}), 404

    temporada_api = temporada.to_api_model()
    capitulos_json = [capitulo for capitulo in temporada_api.capitulos]
    return jsonify(capitulos_json), 200

@app.route('/series/<serie_id>/temporadas/<temporada_id>/capitulos/<capitulo_id>', methods=['GET'])
def obtener_capitulo(serie_id, temporada_id, capitulo_id):  # noqa: E501
    """Obtener un capítulo específico de una temporada

    Obtiene la información detallada de un capítulo específico de una temporada de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int
    :param capitulo_id: ID del capítulo
    :type capitulo_id: int

    :rtype: Union[Capitulo, Tuple[Capitulo, int], Tuple[Capitulo, int, Dict[str, str]]
    """
    serie = SerieDB.objects(id=ObjectId(serie_id)).first()
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    temporada = next((temporada for temporada in serie.temporadas if temporada.temporada_id == ObjectId(temporada_id)), None)
    if not temporada:
        return jsonify({"message": "Temporada no encontrada", "status": "error"}), 404

    capitulo = next((capitulo for capitulo in temporada.capitulos if capitulo.capitulo_id == ObjectId(capitulo_id)), None)
    if not capitulo:
        return jsonify({"message": "Capítulo no encontrado", "status": "error"}), 404

    return jsonify(capitulo.to_api_model()), 200

@app.route('/obtener_lista_capitulos', methods=['GET'])
def obtener_lista_capitulos():
    if request.is_json:
        lista_ids = request.get_json()
    else: 
        return jsonify({"message": "Error al obtener la lista de capítulos", "status": "error"}), 400

    lista_capitulos = []
    for capitulo_id in lista_ids:
        serie = SerieDB.objects(temporadas__capitulos__capitulo_id=ObjectId(capitulo_id)).first()
        if not serie:
            return jsonify({"message": "Capítulo no encontrado", "status": "error"}), 404

        for temporada in serie.temporadas:
            capitulo = next((capitulo for capitulo in temporada.capitulos if capitulo.capitulo_id == ObjectId(capitulo_id)), None)
            if capitulo:
                custom_data = {
                    "nombre_serie": serie.titulo,
                    "num_temporada": temporada.numero,
                    "capitulo_id": str(capitulo.capitulo_id),
                    "nombre_capitulo": capitulo.titulo,
                    "numero_capitulo": capitulo.numero
                }
                lista_capitulos.append(custom_data)
                break

    return jsonify(lista_capitulos), 200