from datetime import date, datetime  # noqa: F401

from typing import List, Dict

from openapi_server.models.base_model import Model
from openapi_server.models.perfil import Perfil  # noqa: E501

from openapi_server import util


class Dispositivo(Model):
    """
      NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
    	Do not edit the class manually.
    """

    def __init__(self, nombre=None):  # noqa: E501
        """Dispositivo - a model defined in OpenAPI

        :param nombre: The nombre of this Dispositivo.  # noqa: E501
        :type nombre: str
        """
        self.openapi_types = {
            'nombre': str,
        }

        self.attribute_map = {
            'nombre': 'nombre',
        }

        self._nombre = nombre

    def serialize(self):
        return {
            'nombre': self.nombre,
        }

    @classmethod
    def from_dict(cls, dikt) -> 'Dispositivo':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Dispositivo of this Dispositivo.  # noqa: E501
        :rtype: Dispositivo
        """
        return util.deserialize_model(dikt, cls)

    @property
    def nombre(self) -> str:
         """Gets the nombre of this Dispositivo.
    
         :return: The nombre of this Dispositivo.
         :rtype: str
         """
         return self._nombre
    
    @nombre.setter
    def nombre(self, nombre: str):
         """Sets the nombre of this Dispositivo.
    
         :param nombre: The nombre of this Dispositivo.
         :type nombre: str
         """
         if nombre is None:
             raise ValueError("Invalid value for `nombre`, must not be `None`")  # noqa: E501
    
         self._nombre = nombre