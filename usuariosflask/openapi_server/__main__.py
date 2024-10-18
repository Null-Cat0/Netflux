#!/usr/bin/env python3
from openapi_server.controllers import usuario_controller

from openapi_server import db
from openapi_server import connex_app, app
from flask import render_template

# Definir una ruta básica para verificar que la app funcione
@app.route('/')
def home():
    return render_template("inicio_sesion.html")

# Punto de entrada principal
if __name__ == '__main__':
    # Crear las tablas de la base de datos al inicio de la app
    with app.app_context():
        db.create_all()
    connex_app.run(port=8080)
