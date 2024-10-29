from openapi_server.models.base_model import Model

from openapi_server import util


class Dispositivo(Model):
    """
      NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
    	Do not edit the class manually.
    """

    def __init__(self, tipo_dispositivo=None):  # noqa: E501
        """Dispositivo - a model defined in OpenAPI

        :param nombre: The nombre of this Dispositivo.  # noqa: E501
        :type nombre: str
        """
        self.openapi_types = {
            'tipo_dispositivo': str,
        }

        self.attribute_map = {
            'tipo_dispositivo': 'tipo',
        }

        self._tipo_dispositivo = tipo_dispositivo

    def serialize(self):
        return {
            'tipo_dispositivo': self._tipo_dispositivo
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
    def tipo_dispositivo(self) -> str:
         """Gets the nombre of this Dispositivo.
    
         :return: The nombre of this Dispositivo.
         :rtype: str
         """
         return self._tipo_dispositivo
    
    @tipo_dispositivo.setter
    def nombre(self, tipo_dispositivo: str):
         """Sets the nombre of this Dispositivo.
    
         :param nombre: The nombre of this Dispositivo.
         :type nombre: str
         """
         if tipo_dispositivo is None:
             raise ValueError("Invalid value for `nombre`, must not be `None`")  # noqa: E501
    
         self._tipo_dispositivo = tipo_dispositivo
