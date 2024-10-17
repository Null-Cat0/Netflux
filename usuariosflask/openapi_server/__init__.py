# Configuración de Flask y la base de datos
import connexion
from flask_sqlalchemy import SQLAlchemy
from openapi_server.encoder import CustomJSONEncoder


connex_app = connexion.App(__name__, specification_dir='./openapi/')
app = connex_app.app  # Asocia la app de Flask con la de Connexion
app.secret_key = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de la base de datos
db = SQLAlchemy(app)

# from openapi_server.controllers import usuario_controller

# Usar el codificador personalizado
app.json_encoder = CustomJSONEncoder

# Añadir la API
connex_app.add_api('openapi.yaml', arguments={'title': 'Netflux Grupo 3 - OpenAPI 3.0'}, pythonic_params=True)
