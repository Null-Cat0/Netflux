from openapi_server.models.base_model import Model
from openapi_server import util


class Genero(Model):
    """
      NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
    	Do not edit the class manually.
    """

    def __init__(self, nombre=None):  # noqa: E501
        """Genero - a model defined in OpenAPI

        :param nombre: The nombre of this Genero.  # noqa: E501
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
            'nombre': self._nombre
        }

    @classmethod
    def from_dict(cls, dikt) -> 'Genero':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Genero.  # noqa: E501
        :rtype: Genero
        """
        return util.deserialize_model(dikt, cls)

    @property
    def nombre(self) -> str:
         """Gets the nombre of this Genero.
    
         :return: The nombre of this Genero.
         :rtype: str
         """
         return self._nombre
    
    @nombre.setter
    def nombre(self, nombre: str):
         """Sets the nombre of this Genero.
    
         :param nombre: The nombre of this Genero.
         :type nombre: str
         """
         if nombre is None:
             raise ValueError("Invalid value for `nombre`, must not be `None`")  # noqa: E501
    
         self._nombre = nombre