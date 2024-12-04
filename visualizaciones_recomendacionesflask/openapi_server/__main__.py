#!/usr/bin/env python3
from openapi_server import connex_app, app

from openapi_server.config import VisualizacionesConfig

if __name__ == '__main__':
    connex_app.run(host="0.0.0.0", port=VisualizacionesConfig.VISUALIZACIONES_PORT)