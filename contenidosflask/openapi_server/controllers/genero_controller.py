from openapi_server import app

from openapi_server.models.genero import Genero
from openapi_server.models.genero_db import GeneroDB

from flask import jsonify, request
from bson import ObjectId

@app.route('/generos/<genero_id>', methods=['PUT'])
def actualizar_genero(genero_id):  # noqa: E501
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

@app.route('/generos', methods=['GET'])
def listar_generos():  # noqa: E501
    generos_db = GeneroDB.objects()
    list_generos_api = [genero.to_api_model().serialize() for genero in generos_db]
    return jsonify(list_generos_api), 200

@app.route('/generos/<genero_id>', methods=['GET'])
def obtener_genero(genero_id):  # noqa: E501
    genero_db = GeneroDB.objects(id=ObjectId(genero_id)).first()
    if not genero_db:
        return jsonify({"message": "Género no encontrado", "status": "error"}), 404

    return jsonify(genero_db.to_api_model().serialize()), 200
