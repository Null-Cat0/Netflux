#!/usr/bin/env python3
import connexion
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Importa tu codificador personalizado
from openapi_server.encoder import CustomJSONEncoder  # Asegúrate de que la ruta sea correcta

# Configuración de Flask y la base de datos
connex_app = connexion.App(__name__, specification_dir='./openapi/')
app = connex_app.app  # Asocia la app de Flask con la de Connexion
app.secret_key = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visualizaciones_recomendaciones.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de la base de datos
db = SQLAlchemy(app)

# Usar el codificador personalizado
app.json_encoder = CustomJSONEncoder

# Añadir la API
connex_app.add_api('openapi.yaml', arguments={'title': 'Netflux Grupo 3 - OpenAPI 3.0'}, pythonic_params=True)

# Crear las tablas de la base de datos al inicio de la app
with app.app_context():
    db.create_all()

# Definir una ruta básica para verificar que la app funcione
@app.route('/')
def home():
    return "Hello, Flask with Connexion and SQLAlchemy!"

# Punto de entrada principal
if __name__ == '__main__':
    connex_app.run(port=8080)
