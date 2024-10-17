import unittest

from flask import json

from openapi_server.models.recomendacion import Recomendacion  # noqa: E501
from openapi_server.test import BaseTestCase


class TestRecomendacionController(BaseTestCase):
    """RecomendacionController integration test stubs"""

    def test_crear_recomendacion_perfil(self):
        """Test case for crear_recomendacion_perfil

        Crea una recomendación para un perfil
        """
        recomendacion = {"contenido_recomendado":[{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."},{"numero":1,"titulo":"Piloto","duracion":58,"id":1,"sinopsis":"Walter White toma una decisión radical tras ser diagnosticado con cáncer de pulmón."}],"id_recomendacion":1,"id_perfil":1}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/perfil/{perfil_id}/recomendaciones'.format(perfil_id=1),
            method='POST',
            headers=headers,
            data=json.dumps(recomendacion),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_eliminar_recomendacion_perfil(self):
        """Test case for eliminar_recomendacion_perfil

        Elimina una recomendación en específico de un perfil
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/perfil/{perfil_id}/recomendaciones/{recomendacion_id}'.format(perfil_id=1, recomendacion_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_recomendacion_perfil(self):
        """Test case for obtener_recomendacion_perfil

        Obtiene una recomendación en específico de un perfil
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/perfil/{perfil_id}/recomendaciones/{recomendacion_id}'.format(perfil_id=1, recomendacion_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_recomendaciones_perfil(self):
        """Test case for obtener_recomendaciones_perfil

        Obtiene una lista de las recomendaciones para el perfil
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/perfil/{perfil_id}/recomendaciones'.format(perfil_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
