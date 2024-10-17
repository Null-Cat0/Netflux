import unittest

from flask import json

from openapi_server.models.actor import Actor  # noqa: E501
from openapi_server.models.actor_update import ActorUpdate  # noqa: E501
from openapi_server.models.pelicula import Pelicula  # noqa: E501
from openapi_server.models.serie import Serie  # noqa: E501
from openapi_server.test import BaseTestCase


class TestActorController(BaseTestCase):
    """ActorController integration test stubs"""

    def test_actualizar_actor(self):
        """Test case for actualizar_actor

        Actualizar un actor existente
        """
        actor_update = {"fechaNacimiento":"1956-03-07","biografia":"Actor estadounidense conocido por su papel en 'Breaking Bad'.","id":1,"nombre":"Bryan Cranston"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/actores/{actor_id}'.format(actor_id=1),
            method='PUT',
            headers=headers,
            data=json.dumps(actor_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_crear_actor(self):
        """Test case for crear_actor

        Crear un nuevo actor
        """
        actor = {"fechaNacimiento":"1956-03-07","biografia":"Actor estadounidense conocido por su papel en 'Breaking Bad'.","id":1,"nombre":"Bryan Cranston"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/actores',
            method='POST',
            headers=headers,
            data=json.dumps(actor),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_eliminar_actor(self):
        """Test case for eliminar_actor

        Eliminar un actor
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/actores/{actor_id}'.format(actor_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_actores(self):
        """Test case for listar_actores

        Listar todos los actores
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/actores',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_peliculas_de_actor(self):
        """Test case for listar_peliculas_de_actor

        Listar películas en las que ha participado un actor en específico.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/actores/{actor_id}/peliculas'.format(actor_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_series_de_actor(self):
        """Test case for listar_series_de_actor

        Listar series en las que ha participado un actor en específico.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/actores/{actor_id}/series'.format(actor_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_actor(self):
        """Test case for obtener_actor

        Obtener un actor específico
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/actores/{actor_id}'.format(actor_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
