#!/usr/bin/env python3

from openapi_server import connex_app, app

if __name__ == '__main__':
    connex_app.run(port=8081)
