from openapi_server import app

from openapi_server.models.genero import Genero
from openapi_server.models.genero_db import GeneroDB

from flask import jsonify, request
from bson import ObjectId

@app.route('/actualizar_genero/<genero_id>', methods=['PUT'])
def actualizar_genero(genero_id):  # noqa: E501
    """Actualizar un género existente

    Actualiza la información de un género específico por su ID. # noqa: E501

    :rtype: dict
    """
    if request.is_json:
        genero_api = Genero.from_dict(request.get_json())
        genero_to_update = GeneroDB.objects(id=ObjectId(genero_id)).first()
        
        if not genero_to_update:
            return jsonify({"message": "Género no encontrado", "status": "error"}), 404

        if genero_api and genero_api.nombre:
            if GeneroDB.objects(nombre=genero_api.nombre, id__ne=genero_id).first():
                return jsonify({"message": "Ya existe otro género con ese nombre", "status": "error"}), 400
            
            genero_to_update.nombre = genero_api.nombre
            genero_to_update.save()
            return jsonify({"message": "Género actualizado con éxito", "status": "success"}), 200
        else:
            return jsonify({"message": "El nombre del género es obligatorio", "status": "error"}), 400
    else:
        return jsonify({"message": "Datos inválidos o malformados", "status": "error"}), 400


@app.route('/listar_generos', methods=['GET'])
def listar_generos():  # noqa: E501
    """Listar todos los géneros

    Obtiene una lista de todos los géneros registrados en el sistema. # noqa: E501

    :rtype: List[dict]
    """
    generos_db = GeneroDB.objects()
    list_generos_api = [genero.to_api_model().serialize() for genero in generos_db]
    return jsonify(list_generos_api), 200


@app.route('/obtener_genero/<genero_id>', methods=['GET'])
def obtener_genero(genero_id):  # noqa: E501
    """Obtener un género específico

    Obtiene la información detallada de un género específico por su ID. # noqa: E501

    :rtype: dict
    """
    genero_db = GeneroDB.objects(id=ObjectId(genero_id)).first()
    if not genero_db:
        return jsonify({"message": "Género no encontrado", "status": "error"}), 404

    return jsonify(genero_db.to_api_model().serialize()), 200

# @app.route('/obtener_lista_generos', methods=['GET'])
# def obtener_lista_generos():
#     if request.is_json:
#         lista_ids = request.get_json()
#     else:
#         return jsonify({"message": "Error al obtener la lista de géneros", "status": "error"}), 400
#     lista_generos = GeneroDB.objects(id__in=lista_ids)
#     lista_generos_api = [genero.to_api_model() for genero in lista_generos]
#     return jsonify(lista_generos_api), 200

