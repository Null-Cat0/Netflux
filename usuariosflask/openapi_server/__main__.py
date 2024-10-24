#!/usr/bin/env python3
from sqlalchemy import values
from openapi_server.controllers import usuario_controller

from openapi_server import db
from openapi_server import util
from openapi_server import connex_app, app

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from openapi_server.models import usuario
from openapi_server.models.usuario_db import UsuarioDB

# Definir una ruta básica para verificar que la app funcione
@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    """Verifica las credenciales del usuario y responde con un mensaje JSON."""
    data = request.json
    correo_electronico = data.get('correo_electronico')
    password = data.get('password')

    usuario = UsuarioDB.query.filter_by(correo_electronico=correo_electronico).first()

    if usuario is None:
        return jsonify({"message": "El correo introducido no existe", "status": "error"}), 404
    elif usuario.password != password:
        return jsonify({"message": "Contraseña inválida", "status": "error"}), 401
    else:
        return jsonify({"message": "Inicio de sesión exitoso", "status": "success", "user_id": usuario.user_id}), 200

"""
@app.route('/')
def home():
    return redirect(url_for('login'))
"""

# Punto de entrada principal
if __name__ == '__main__':
    # Crear las tablas de la base de datos al inicio de la app
    with app.app_context():
        # Mock up
        if not db.inspect(db.engine).has_table('dispositivos_usuario_db'):
            db.create_all()
            util.populate_dispositivosDB()
        else:
            db.create_all()

    connex_app.run(port=8080)
