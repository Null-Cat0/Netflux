#!/usr/bin/env python3
from openapi_server import connex_app, util
from openapi_server.config import ContenidosConfig

if __name__ == '__main__':
    util.populate_genresDB()
    connex_app.run(host="0.0.0.0", port=ContenidosConfig.CONTENIDOS_PORT)
