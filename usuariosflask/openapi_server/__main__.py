#!/usr/bin/env python3
from openapi_server.controllers import usuario_controller

from openapi_server import db
from openapi_server import connex_app, app

# Definir una ruta básica para verificar que la app funcione
@app.route('/')
def home():
    return "Hello, Flask with Connexion and SQLAlchemy!"

# Punto de entrada principal
if __name__ == '__main__':
    # Crear las tablas de la base de datos al inicio de la app
    with app.app_context():
        db.drop_all()
        db.create_all()
    connex_app.run(port=8080)
