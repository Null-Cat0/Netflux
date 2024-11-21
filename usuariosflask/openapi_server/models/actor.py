from openapi_server import util
from openapi_server.models.base_model import Model

from datetime import date


class Actor(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, nombre=None, fecha_nacimiento=None, biografia=None):  # noqa: E501
        """Actor - a model defined in OpenAPI

        :param id: The id of this Actor.  # noqa: E501
        :type id: int
        :param nombre: The nombre of this Actor.  # noqa: E501
        :type nombre: str
        :param fecha_nacimiento: The fecha_nacimiento of this Actor.  # noqa: E501
        :type fecha_nacimiento: date
        :param biografia: The biografia of this Actor.  # noqa: E501
        :type biografia: str
        """
        self.openapi_types = {
            'id': int,
            'nombre': str,
            'fecha_nacimiento': date,
            'biografia': str
        }

        self.attribute_map = {
            'id': 'id',
            'nombre': 'nombre',
            'fecha_nacimiento': 'fechaNacimiento',
            'biografia': 'biografia'
        }

        self._id = id
        self._nombre = nombre
        self._fecha_nacimiento = fecha_nacimiento
        self._biografia = biografia

    @classmethod
    def from_dict(cls, dikt) -> 'Actor':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Actor of this Actor.  # noqa: E501
        :rtype: Actor
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Actor.


        :return: The id of this Actor.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Actor.


        :param id: The id of this Actor.
        :type id: int
        """

        self._id = id

    @property
    def nombre(self) -> str:
        """Gets the nombre of this Actor.


        :return: The nombre of this Actor.
        :rtype: str
        """
        return self._nombre

    @nombre.setter
    def nombre(self, nombre: str):
        """Sets the nombre of this Actor.


        :param nombre: The nombre of this Actor.
        :type nombre: str
        """
        if nombre is None:
            raise ValueError("Invalid value for `nombre`, must not be `None`")  # noqa: E501

        self._nombre = nombre

    @property
    def fecha_nacimiento(self) -> date:
        """Gets the fecha_nacimiento of this Actor.


        :return: The fecha_nacimiento of this Actor.
        :rtype: date
        """
        return self._fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, fecha_nacimiento: date):
        """Sets the fecha_nacimiento of this Actor.


        :param fecha_nacimiento: The fecha_nacimiento of this Actor.
        :type fecha_nacimiento: date
        """
        if fecha_nacimiento is None:
            raise ValueError("Invalid value for `fecha_nacimiento`, must not be `None`")  # noqa: E501

        self._fecha_nacimiento = fecha_nacimiento

    @property
    def biografia(self) -> str:
        """Gets the biografia of this Actor.


        :return: The biografia of this Actor.
        :rtype: str
        """
        return self._biografia

    @biografia.setter
    def biografia(self, biografia: str):
        """Sets the biografia of this Actor.


        :param biografia: The biografia of this Actor.
        :type biografia: str
        """
        if biografia is None:
            raise ValueError("Invalid value for `biografia`, must not be `None`")  # noqa: E501

        self._biografia = biografia
