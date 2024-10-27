#!/usr/bin/env python3
from openapi_server import db
from openapi_server import util
from openapi_server import connex_app, app

from flask import request, jsonify

from openapi_server.models.usuario_db import UsuarioDB

# Definir una ruta básica para verificar que la app funcione
@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    """Verifica las credenciales del usuario y responde con un mensaje JSON."""
    data = request.json
    correo_electronico = data.get('correo_electronico')
    password = data.get('password')

    usuario_db = UsuarioDB.query.filter_by(correo_electronico=correo_electronico).first()
    usuario = usuario_db.to_api_model()

    if usuario is None:
        return jsonify({"message": "El correo introducido no existe", "status": "error"}), 404
    elif usuario.password != password:
        return jsonify({"message": "Contraseña inválida", "status": "error"}), 401
    else:
        return jsonify({"message": "Inicio de sesión exitoso", "status": "success", "usuario": usuario.serialize()}), 200

"""
@app.route('/')
def home():
    return redirect(url_for('login'))
"""

# Punto de entrada principal
if __name__ == '__main__':
    # Crear las tablas de la base de datos al inicio de la app
    with app.app_context():
        db.create_all()
        util.populate_dispositivosDB()

    connex_app.run(port=8080)
