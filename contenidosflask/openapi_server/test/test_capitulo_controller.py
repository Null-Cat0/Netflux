import unittest

from flask import json

from openapi_server.models.capitulo import Capitulo  # noqa: E501
from openapi_server.models.capitulo_update import CapituloUpdate  # noqa: E501
from openapi_server.test import BaseTestCase


class TestCapituloController(BaseTestCase):
    """CapituloController integration test stubs"""

    def test_actualizar_capitulo(self):
        """Test case for actualizar_capitulo

        Actualizar un capítulo existente
        """
        capitulo_update = {"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/temporadas/{temporada_id}/capitulos/{capitulo_id}'.format(serie_id=1, temporada_id=1, capitulo_id=1),
            method='PUT',
            headers=headers,
            data=json.dumps(capitulo_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_crear_capitulo(self):
        """Test case for crear_capitulo

        Crear un nuevo capítulo para una temporada
        """
        capitulo = {"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/temporadas/{temporada_id}/capitulos'.format(serie_id=1, temporada_id=1),
            method='POST',
            headers=headers,
            data=json.dumps(capitulo),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_eliminar_capitulo(self):
        """Test case for eliminar_capitulo

        Eliminar un capítulo
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/temporadas/{temporada_id}/capitulos/{capitulo_id}'.format(serie_id=1, temporada_id=1, capitulo_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_capitulos(self):
        """Test case for listar_capitulos

        Listar todos los capítulos de una temporada
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/temporadas/{temporada_id}/capitulos'.format(serie_id=1, temporada_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_capitulo(self):
        """Test case for obtener_capitulo

        Obtener un capítulo específico de una temporada
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/series/{serie_id}/temporadas/{temporada_id}/capitulos/{capitulo_id}'.format(serie_id=1, temporada_id=1, capitulo_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
