import unittest

from flask import json

from openapi_server.models.perfil import Perfil  # noqa: E501
from openapi_server.models.perfil_update import PerfilUpdate  # noqa: E501
from openapi_server.models.serie import Serie  # noqa: E501
from openapi_server.test import BaseTestCase


class TestPerfilController(BaseTestCase):
    """PerfilController integration test stubs"""

    def test_actualizar_perfil_usuario(self):
        """Test case for actualizar_perfil_usuario

        Actualiza el perfil especificado
        """
        perfil_update = {"user_id":3,"preferencias_contenido":{"languages":["Espanol"],"genres":["Action","Supernatural"]},"foto_perfil":"path/to/image","id":1,"nombre":"Euler","historial_vistos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"mi_lista":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}]}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/usuario/{user_id}/perfiles/{profile_id}'.format(user_id=1, profile_id=1),
            method='PUT',
            headers=headers,
            data=json.dumps(perfil_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_borrar_perfil_usuario(self):
        """Test case for borrar_perfil_usuario

        Borra el perfil especificado
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/usuario/{user_id}/perfiles/{profile_id}'.format(user_id=1, profile_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_crear_perfil(self):
        """Test case for crear_perfil

        Añade un nuevo perfil al usuario especificado
        """
        perfil = {"user_id":3,"preferencias_contenido":{"languages":["Espanol"],"genres":["Action","Supernatural"]},"foto_perfil":"path/to/image","id":1,"nombre":"Euler","historial_vistos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"mi_lista":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}]}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/usuario/{user_id}/perfiles'.format(user_id=1),
            method='POST',
            headers=headers,
            data=json.dumps(perfil),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_historial_perfil(self):
        """Test case for obtener_historial_perfil

        Obtiene el historial de contenido completado por de un perfil
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/usuario/{user_id}/perfiles/{profile_id}/historial'.format(user_id=1, profile_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_lista_perfil(self):
        """Test case for obtener_lista_perfil

        Obtiene la lista de un perfil concreto
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/usuario/{user_id}/perfiles/{profile_id}/lista'.format(user_id=1, profile_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_perfil_usuario(self):
        """Test case for obtener_perfil_usuario

        Obtiene el perfil específico de un usuario concreto
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/usuario/{user_id}/perfiles/{profile_id}'.format(user_id=1, profile_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_perfiles(self):
        """Test case for obtener_perfiles

        Obtiene todos los perfiles del usuario especificado
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/usuario/{user_id}/perfiles'.format(user_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
