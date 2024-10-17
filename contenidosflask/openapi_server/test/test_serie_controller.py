import unittest

from flask import json

from openapi_server.models.actor import Actor  # noqa: E501
from openapi_server.models.asignar_actor_a_serie_request import AsignarActorASerieRequest  # noqa: E501
from openapi_server.models.serie import Serie  # noqa: E501
from openapi_server.models.serie_update import SerieUpdate  # noqa: E501
from openapi_server.test import BaseTestCase


class TestSerieController(BaseTestCase):
    """SerieController integration test stubs"""

    def test_actualizar_serie(self):
        """Test case for actualizar_serie

        Actualizar una serie existente
        """
        serie_update = {"actores":[{"fechaNacimiento":"1956-03-07","biografia":"Actor estadounidense conocido por su papel en 'Breaking Bad'.","id":1,"nombre":"Bryan Cranston"},{"fechaNacimiento":"1956-03-07","biografia":"Actor estadounidense conocido por su papel en 'Breaking Bad'.","id":1,"nombre":"Bryan Cranston"}],"temporadas":[{"capitulos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"numero":1,"anioLanzamiento":2008,"id":1},{"capitulos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"numero":1,"anioLanzamiento":2008,"id":1}],"genero":"Drama","titulo":"Breaking Bad","anioEstreno":2008,"id":1,"sinopsis":"Un profesor de química se convierte en fabricante de metanfetamina."}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}'.format(serie_id=1),
            method='PUT',
            headers=headers,
            data=json.dumps(serie_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_asignar_actor_a_serie(self):
        """Test case for asignar_actor_a_serie

        Asignar un actor a una serie
        """
        asignar_actor_a_serie_request = openapi_server.AsignarActorASerieRequest()
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/actores'.format(serie_id=1),
            method='PATCH',
            headers=headers,
            data=json.dumps(asignar_actor_a_serie_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_crear_serie(self):
        """Test case for crear_serie

        Crear una nueva serie
        """
        serie = {"actores":[{"fechaNacimiento":"1956-03-07","biografia":"Actor estadounidense conocido por su papel en 'Breaking Bad'.","id":1,"nombre":"Bryan Cranston"},{"fechaNacimiento":"1956-03-07","biografia":"Actor estadounidense conocido por su papel en 'Breaking Bad'.","id":1,"nombre":"Bryan Cranston"}],"temporadas":[{"capitulos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"numero":1,"anioLanzamiento":2008,"id":1},{"capitulos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"numero":1,"anioLanzamiento":2008,"id":1}],"genero":"Drama","titulo":"Breaking Bad","anioEstreno":2008,"id":1,"sinopsis":"Un profesor de química se convierte en fabricante de metanfetamina."}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series',
            method='POST',
            headers=headers,
            data=json.dumps(serie),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_eliminar_actor_serie(self):
        """Test case for eliminar_actor_serie

        Elimnar un actor de una serie
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/actores/{actor_id}'.format(serie_id=1, actor_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_eliminar_serie(self):
        """Test case for eliminar_serie

        Eliminar una serie
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}'.format(serie_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_actores_de_serie(self):
        """Test case for listar_actores_de_serie

        Listar los actores de una serie específica
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/actores'.format(serie_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_series(self):
        """Test case for listar_series

        Listar todas las series
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_serie(self):
        """Test case for obtener_serie

        Obtener una serie específica
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}'.format(serie_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
