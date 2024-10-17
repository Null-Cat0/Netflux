import unittest

from flask import json

from openapi_server.models.temporada import Temporada  # noqa: E501
from openapi_server.models.temporada_update import TemporadaUpdate  # noqa: E501
from openapi_server.test import BaseTestCase


class TestTemporadaController(BaseTestCase):
    """TemporadaController integration test stubs"""

    def test_actualizar_temporada(self):
        """Test case for actualizar_temporada

        Actualizar una temporada existente
        """
        temporada_update = {"capitulos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"numero":1,"anioLanzamiento":2008,"id":1}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/temporadas/{temporada_id}'.format(serie_id=1, temporada_id=1),
            method='PUT',
            headers=headers,
            data=json.dumps(temporada_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_crear_temporada(self):
        """Test case for crear_temporada

        Crear una nueva temporada para una serie
        """
        temporada = {"capitulos":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"numero":1,"anioLanzamiento":2008,"id":1}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/temporadas'.format(serie_id=1),
            method='POST',
            headers=headers,
            data=json.dumps(temporada),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_eliminar_temporada(self):
        """Test case for eliminar_temporada

        Eliminar una temporada
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/temporadas/{temporada_id}'.format(serie_id=1, temporada_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_temporadas(self):
        """Test case for listar_temporadas

        Listar todas las temporadas de una serie
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/temporadas'.format(serie_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_temporada(self):
        """Test case for obtener_temporada

        Obtener una temporada específica de una serie
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/temporadas/{temporada_id}'.format(serie_id=1, temporada_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
