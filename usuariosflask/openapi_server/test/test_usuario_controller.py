import unittest

from flask import json

from openapi_server.models.usuario import Usuario  # noqa: E501
from openapi_server.models.usuario_update import UsuarioUpdate  # noqa: E501
from openapi_server.test import BaseTestCase


class TestUsuarioController(BaseTestCase):
    """UsuarioController integration test stubs"""

    def test_actualizar_usuario(self):
        """Test case for actualizar_usuario

        Actualizar un usuario existente
        """
        usuario_update = {"dispositivos":["Móvil","TV"],"correo_electronico":"juan@gmail.com","plan_suscripcion":"Básico","perfiles":[{"user_id":3,"preferencias_contenido":{"languages":["Espanol"],"genres":["Action","Supernatural"]},"foto_perfil":"path/to/image","id":1,"nombre":"Euler","historial_vistos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"mi_lista":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}]},{"user_id":3,"preferencias_contenido":{"languages":["Espanol"],"genres":["Action","Supernatural"]},"foto_perfil":"path/to/image","id":1,"nombre":"Euler","historial_vistos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"mi_lista":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}]}],"id":1,"nombre":"Juan Miguel León Rojas","pais":"España"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/usuario/{user_id}'.format(user_id=1),
            method='PUT',
            headers=headers,
            data=json.dumps(usuario_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_crear_usuario(self):
        """Test case for crear_usuario

        Crear un nuevo usuario
        """
        usuario = {"dispositivos":["Móvil","TV"],"correo_electronico":"juan@gmail.com","plan_suscripcion":"Básico","perfiles":[{"user_id":3,"preferencias_contenido":{"languages":["Espanol"],"genres":["Action","Supernatural"]},"foto_perfil":"path/to/image","id":1,"nombre":"Euler","historial_vistos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"mi_lista":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}]},{"user_id":3,"preferencias_contenido":{"languages":["Espanol"],"genres":["Action","Supernatural"]},"foto_perfil":"path/to/image","id":1,"nombre":"Euler","historial_vistos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"mi_lista":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}]}],"id":1,"nombre":"Juan Miguel León Rojas","pais":"España"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/usuario',
            method='POST',
            headers=headers,
            data=json.dumps(usuario),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_eliminar_usuario(self):
        """Test case for eliminar_usuario

        Eliminar un usuario
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/usuario/{user_id}'.format(user_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_usuarios(self):
        """Test case for listar_usuarios

        Listar todos los usuarios
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/usuario',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_usuario(self):
        """Test case for obtener_usuario

        Obtener un usuario específico
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/usuario/{user_id}'.format(user_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
