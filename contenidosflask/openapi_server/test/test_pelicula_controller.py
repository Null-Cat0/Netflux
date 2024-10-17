import unittest

from flask import json

from openapi_server.models.actor import Actor  # noqa: E501
from openapi_server.models.asignar_actor_a_serie_request import AsignarActorASerieRequest  # noqa: E501
from openapi_server.models.pelicula import Pelicula  # noqa: E501
from openapi_server.models.pelicula_update import PeliculaUpdate  # noqa: E501
from openapi_server.test import BaseTestCase


class TestPeliculaController(BaseTestCase):
    """PeliculaController integration test stubs"""

    def test_actualizar_pelicula(self):
        """Test case for actualizar_pelicula

        Actualizar una película existente
        """
        pelicula_update = {"actores":[{"fechaNacimiento":"1956-03-07","biografia":"Actor estadounidense conocido por su papel en 'Breaking Bad'.","id":1,"nombre":"Bryan Cranston"},{"fechaNacimiento":"1956-03-07","biografia":"Actor estadounidense conocido por su papel en 'Breaking Bad'.","id":1,"nombre":"Bryan Cranston"}],"temporadas":[{"capitulos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"numero":1,"anioLanzamiento":2008,"id":1},{"capitulos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"numero":1,"anioLanzamiento":2008,"id":1}],"genero":"Drama","titulo":"Breaking Bad","duracion":112,"anioEstreno":2008,"id":1,"sinopsis":"Un profesor de química se convierte en fabricante de metanfetamina."}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/pelicula/{pelicula_id}'.format(pelicula_id=1),
            method='PUT',
            headers=headers,
            data=json.dumps(pelicula_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_asignar_actor_a_pelicula(self):
        """Test case for asignar_actor_a_pelicula

        Asignar un actor a una película
        """
        asignar_actor_a_serie_request = openapi_server.AsignarActorASerieRequest()
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/pelicula/{pelicula_id}/actores'.format(pelicula_id=1),
            method='PATCH',
            headers=headers,
            data=json.dumps(asignar_actor_a_serie_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_crear_pelicula(self):
        """Test case for crear_pelicula

        Crear una nueva película
        """
        pelicula = {"actores":[{"fechaNacimiento":"1956-03-07","biografia":"Actor estadounidense conocido por su papel en 'Breaking Bad'.","id":1,"nombre":"Bryan Cranston"},{"fechaNacimiento":"1956-03-07","biografia":"Actor estadounidense conocido por su papel en 'Breaking Bad'.","id":1,"nombre":"Bryan Cranston"}],"temporadas":[{"capitulos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"numero":1,"anioLanzamiento":2008,"id":1},{"capitulos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"numero":1,"anioLanzamiento":2008,"id":1}],"genero":"Drama","titulo":"Breaking Bad","duracion":112,"anioEstreno":2008,"id":1,"sinopsis":"Un profesor de química se convierte en fabricante de metanfetamina."}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/pelicula',
            method='POST',
            headers=headers,
            data=json.dumps(pelicula),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_eliminar_actor_pelicula(self):
        """Test case for eliminar_actor_pelicula

        Elimnar un actor de una película
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/pelicula/{pelicula_id}/actores/{actor_id}'.format(pelicula_id=1, actor_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_eliminar_pelicula(self):
        """Test case for eliminar_pelicula

        Eliminar una película
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/pelicula/{pelicula_id}'.format(pelicula_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_actores_de_pelicula(self):
        """Test case for listar_actores_de_pelicula

        Listar actores de una película específica
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/pelicula/{pelicula_id}/actores'.format(pelicula_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_peliculas(self):
        """Test case for listar_peliculas

        Listar todas las películas
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/pelicula',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_pelicula(self):
        """Test case for obtener_pelicula

        Obtener una película específica
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/pelicula/{pelicula_id}'.format(pelicula_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_precuela_pelicula(self):
        """Test case for obtener_precuela_pelicula

        Obtiene la precuela de una película específica
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/pelicula/{pelicula_id}/precuela'.format(pelicula_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_secuela_pelicula(self):
        """Test case for obtener_secuela_pelicula

        Obtiene la secuela de una película específica
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/pelicula/{pelicula_id}/secuela'.format(pelicula_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
