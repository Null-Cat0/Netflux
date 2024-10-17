import unittest

from flask import json

from openapi_server.models.capitulo import Capitulo  # noqa: E501
from openapi_server.models.pelicula import Pelicula  # noqa: E501
from openapi_server.models.perfil import Perfil  # noqa: E501
from openapi_server.models.visualizacion import Visualizacion  # noqa: E501
from openapi_server.test import BaseTestCase


class TestVisualizacionController(BaseTestCase):
    """VisualizacionController integration test stubs"""

    def test_actualizar_visualizacion_capitulo_perfil(self):
        """Test case for actualizar_visualizacion_capitulo_perfil

        Actualiza la visualización de un capítulo por un perfil
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/visualizacion/{perfil_id}/{capitulo_id}'.format(perfil_id=1, capitulo_id=1),
            method='PATCH',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actualizar_visualizacion_pelicula_perfil(self):
        """Test case for actualizar_visualizacion_pelicula_perfil

        Actualiza la visualización de la película por un perfil
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/visualizacion/{perfil_id}/{pelicula_id}'.format(perfil_id=1, pelicula_id=1),
            method='PATCH',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_crear_visualizacion_contenido_perfil(self):
        """Test case for crear_visualizacion_contenido_perfil

        Inicia la visualización de un capítulo o película por un perfil
        """
        visualizacion = {"fecha_visualizacion":"2002-12-14","id_perfil":1,"id_contenido":1,"progreso":20}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/visualizacion/{perfil_id}'.format(perfil_id=1),
            method='POST',
            headers=headers,
            data=json.dumps(visualizacion),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_visualizaciones_contenido(self):
        """Test case for listar_visualizaciones_contenido

        Lista de perfiles que han visto el contenido especificado
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/visualizacion/{contenido_id}'.format(contenido_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_visualizaciones_perfil(self):
        """Test case for listar_visualizaciones_perfil

        Historial de un perfil en específico
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/visualizacion/{perfil_id}'.format(perfil_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_visualizacion_capitulo_perfil(self):
        """Test case for obtener_visualizacion_capitulo_perfil

        Obtiene el capítulo en visualización del perfil especificado
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/visualizacion/{perfil_id}/{capitulo_id}'.format(perfil_id=1, capitulo_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_visualizacion_pelicula_perfil(self):
        """Test case for obtener_visualizacion_pelicula_perfil

        Obtiene la película visualizada por el perfil especificado
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/visualizacion/{perfil_id}/{pelicula_id}'.format(perfil_id=1, pelicula_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
