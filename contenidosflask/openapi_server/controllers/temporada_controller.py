from openapi_server import app

from openapi_server.models.serie_db import SerieDB
from openapi_server.models.serie import TemporadaEmbedded  # noqa: E501

from flask import jsonify, request
from bson import ObjectId

@app.route('/series/<serie_id>/temporadas/<temporada_id>', methods=['PUT'])
def actualizar_temporada(serie_id, temporada_id):  # noqa: E501
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

@app.route('/series/<serie_id>/temporadas', methods=['POST'])
def crear_temporada(serie_id):  # noqa: E501
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

@app.route('/series/<serie_id>/temporadas/<temporada_id>', methods=['DELETE'])
def eliminar_temporada(serie_id, temporada_id):  # noqa: E501
    serie = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    temporada = next((temporada for temporada in serie.temporadas if temporada.temporada_id == ObjectId(temporada_id)), None)
    if not temporada:
        return jsonify({"message": "Temporada no encontrada", "status": "error"}), 404

    serie.temporadas.remove(temporada)
    serie.save()
    return jsonify({"message": "Temporada eliminada correctamente", "status": "success"}), 200

@app.route('/series/<serie_id>/temporadas', methods=['GET'])
def listar_temporadas(serie_id):  # noqa: E501
    serie = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    serie_api = serie.to_api_model()
    temporadas_json = [temporada for temporada in serie_api.temporadas]
    return jsonify(temporadas_json), 200

@app.route('/series/<serie_id>/temporadas/<temporada_id>', methods=['GET'])
def obtener_temporada(serie_id, temporada_id):  # noqa: E501
    serie = SerieDB.objects.get(id=ObjectId(serie_id))
    if not serie:
        return jsonify({"message": "Serie no encontrada", "status": "error"}), 404

    temporada = next((temporada for temporada in serie.temporadas if temporada.temporada_id == ObjectId(temporada_id)), None)
    if not temporada:
        return jsonify({"message": "Temporada no encontrada", "status": "error"}), 404

    temporada_api = temporada.to_api_model()
    return jsonify(temporada_api), 200