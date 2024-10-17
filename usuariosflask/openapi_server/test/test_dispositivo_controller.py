import unittest

from flask import json

from openapi_server.models.actualizar_dispositivos_request import ActualizarDispositivosRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDispositivoController(BaseTestCase):
    """DispositivoController integration test stubs"""

    def test_actualizar_dispositivos(self):
        """Test case for actualizar_dispositivos

        Actualiza un dispositivo a la lista de dispositivos registrados del usuario
        """
        actualizar_dispositivos_request = openapi_server.ActualizarDispositivosRequest()
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/user/{user_id}/dispositivos'.format(user_id=1),
            method='PATCH',
            headers=headers,
            data=json.dumps(actualizar_dispositivos_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_eliminar_dispositivo(self):
        """Test case for eliminar_dispositivo

        Elimina un dispositivo de la lista de dispositivos registrados del usuario
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/user/{user_id}/dispositivos/{dispositivo_id}'.format(user_id=1, dispositivo_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_dispositivos(self):
        """Test case for obtener_dispositivos

        Obtiene la lista de dispositivos registrados por el usuario
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/user/{user_id}/dispositivos'.format(user_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
