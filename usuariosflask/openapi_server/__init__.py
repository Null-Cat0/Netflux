# Configuración de Flask y la base de datos
import connexion
from flask_sqlalchemy import SQLAlchemy
from openapi_server.encoder import CustomJSONEncoder
from time import sleep

connex_app = connexion.App(__name__, specification_dir='./openapi/')
app = connex_app.app  # Asocia la app de Flask con la de Connexion
app.secret_key = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@mysql:3306/usuarios_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# Inicialización de la base de datos
## Aseguramos que la base de datos esté lista antes de continuar
i = 0
while i < 5:
    try:
        db = SQLAlchemy(app)
        break
    except Exception as e:
        print(e)
        i += 1
        sleep(0.5)

# Usar el codificador personalizado
app.json_encoder = CustomJSONEncoder

# Añadir la API
connex_app.add_api('openapi.yaml', arguments={'title': 'Netflux Grupo 3 - OpenAPI 3.0'}, pythonic_params=True)
