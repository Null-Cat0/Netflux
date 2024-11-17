#!/usr/bin/env python3
from openapi_server import connex_app, app

# Se importa el fichero de configuración de los microservicios
import os, sys, requests
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(app_path)

from global_config import ContenidosConfig

if __name__ == '__main__':
    connex_app.run(port=ContenidosConfig.CONTENIDOS_PORT)
