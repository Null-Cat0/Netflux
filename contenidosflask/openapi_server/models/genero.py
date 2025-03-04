from openapi_server import util
from openapi_server.models.base_model import Model

class Genero(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, nombre=None):  # noqa: E501
        """Genero - a model defined in OpenAPI

        :param id: The id of this Genero.  # noqa: E501
        :type id: int
        :param nombre: The nombre of this Genero.  # noqa: E501
        :type nombre: str
        """
        self.openapi_types = {
            'id': str,
            'nombre': str
        }

        self.attribute_map = {
            'id': 'id',
            'nombre': 'nombre'
        }

        self._id = id
        self._nombre = nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }
    
    def to_db_model(self):
        from openapi_server.models.genero_db import GeneroDB
        return GeneroDB(
            nombre=self._nombre
        )

    @classmethod
    def from_dict(cls, dikt) -> 'Genero':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Genero of this Genero.  # noqa: E501
        :rtype: Genero
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Genero.


        :return: The id of this Genero.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Genero.


        :param id: The id of this Genero.
        :type id: int
        """

        self._id = id

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
