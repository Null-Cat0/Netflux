import connexion
from typing import Dict, Tuple, Union

from openapi_server.models.serie import Serie
from openapi_server.models.serie_db import SerieDB

from openapi_server.models.serie import TemporadaEmbedded  # noqa: E501
from openapi_server.models.serie_db import TemporadaEmbeddedDB

from openapi_server.models.serie import CapituloEmbedded  # noqa: E501
from openapi_server.models.serie_db import CapituloEmbeddedDB

# from openapi_server.models.temporada import Temporada  # noqa: E501
# from openapi_server.models.temporada_update import TemporadaUpdate  # noqa: E501

from openapi_server import app, db, util
from flask import jsonify, request
from bson import ObjectId

@app.route('/actualizar_temporada_serie/<serie_id>/<temporada_id>', methods=['PUT'])
def actualizar_temporada(serie_id, temporada_id):  # noqa: E501
    """Actualizar una temporada existente

    Actualiza la información de una temporada específica de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param numero_temporada: Número de la temporada
    :type numero_temporada: int

    :rtype: dict
    """
    if not request.is_json:
        return jsonify({"message": "Formato de datos no válido", "status": "error"}), 400
    
    # Obtener datos de actualización desde el JSON de la solicitud
    temporada_update_data = TemporadaEmbedded.from_dict(request.get_json())
    
    # Buscar la serie en la base de datos
    serie = SerieDB.objects(id=ObjectId(serie_id)).first()
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    # Buscar la temporada en la lista de temporadas de la serie
    temporada = next((temporada for temporada in serie.temporadas if temporada.temporada_id == ObjectId(temporada_id)), None)
    if not temporada:
        return jsonify({"message": "Temporada no encontrada", "status": "error"}), 404

    # Actualizar los datos de la temporada
    if temporada_update_data.numero and temporada_update_data.numero > -1:
        temporada.numero = temporada_update_data.numero
    if temporada_update_data.anio_lanzamiento:
        temporada.anio_lanzamiento = temporada_update_data.anio_lanzamiento
    if temporada_update_data.capitulos:
        temporada.capitulos = temporada_update_data.capitulos

    # Guardar los cambios en la base de datos
    serie.save()

    return jsonify({"message": "Temporada actualizada correctamente", "status": "success"}), 200

@app.route('/asignar_temporada_serie/<serie_id>', methods=['POST'])
def crear_temporada(serie_id):  # noqa: E501
    """Crear una nueva temporada para una serie

    Crea una nueva temporada para una serie específica. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada: Objeto de la temporada a crear
    :type temporada: dict | bytes

    :rtype: Union[Temporada, Tuple[Temporada, int], Tuple[Temporada, int, Dict[str, str]]
    """
    if request.is_json:
        temporada = TemporadaEmbedded.from_dict(request.get_json())  # noqa: E501

    serie = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    temporada_db = temporada.to_db_model()
    if temporada_db.numero < 0:
        return jsonify({"message": "Número de temporada no válido", "status": "error"}), 400

    serie.temporadas.append(temporada_db)
    serie.save()
    return jsonify({"message": "Temporada creada correctamente", "status": "success"}), 201

@app.route('/eliminar_temporada_serie/<serie_id>/<temporada_id>', methods=['DELETE'])
def eliminar_temporada(serie_id, temporada_id):  # noqa: E501
    """Eliminar una temporada

    Elimina una temporada específica de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    serie = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    temporada = next((temporada for temporada in serie.temporadas if temporada.temporada_id == ObjectId(temporada_id)), None)
    if not temporada:
        return jsonify({"message": "Temporada no encontrada", "status": "error"}), 404

    serie.temporadas.remove(temporada)
    serie.save()
    return jsonify({"message": "Temporada eliminada correctamente", "status": "success"}), 200

@app.route('/listar_temporadas_serie/<serie_id>', methods=['GET'])
def listar_temporadas(serie_id):  # noqa: E501
    """Listar todas las temporadas de una serie

    Obtiene una lista de todas las temporadas de una serie específica. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int

    :rtype: Union[List[Temporada], Tuple[List[Temporada], int], Tuple[List[Temporada], int, Dict[str, str]]
    """
    serie = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    serie_api = serie.to_api_model()
    temporadas_json = [temporada for temporada in serie_api.temporadas]
    return jsonify(temporadas_json), 200

@app.route('/obtener_temporada_serie/<serie_id>/<temporada_id>', methods=['GET'])
def obtener_temporada(serie_id, temporada_id):  # noqa: E501
    """Obtener una temporada específica de una serie

    Obtiene la información detallada de una temporada específica de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int

    :rtype: Union[Temporada, Tuple[Temporada, int], Tuple[Temporada, int, Dict[str, str]]
    """
    serie = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    temporada = next((temporada for temporada in serie.temporadas if temporada.temporada_id == ObjectId(temporada_id)), None)
    if not temporada:
        return jsonify({"message": "Temporada no encontrada", "status": "error"}), 404

    temporada_api = temporada.to_api_model()
    return jsonify(temporada_api), 200