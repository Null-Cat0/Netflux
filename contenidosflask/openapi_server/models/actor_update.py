from openapi_server import util
from openapi_server.models.base_model import Model

from datetime import date


class ActorUpdate(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, nombre=None, fecha_nacimiento=None, nacionalidad=None, biografia=None):  # noqa: E501
        """ActorUpdate - a model defined in OpenAPI

        :param id: The id of this ActorUpdate.  # noqa: E501
        :type id: int
        :param nombre: The nombre of this ActorUpdate.  # noqa: E501
        :type nombre: str
        :param fecha_nacimiento: The fecha_nacimiento of this ActorUpdate.  # noqa: E501
        :type fecha_nacimiento: date
        :param biografia: The biografia of this ActorUpdate.  # noqa: E501
        :type biografia: str
        """
        self.openapi_types = {
            'id': int,
            'nombre': str,
            'fecha_nacimiento': date,
            'nacionalidad': str,
            'biografia': str
        }

        self.attribute_map = {
            'id': 'id',
            'nombre': 'nombre',
            'fecha_nacimiento': 'fecha_nacimiento',
            'nacionalidad': 'nacionalidad',
            'biografia': 'biografia'
        }

        self._id = id
        self._nombre = nombre
        self._fecha_nacimiento = fecha_nacimiento
        self._nacionalidad = nacionalidad
        self._biografia = biografia

    def to_db_model(self):
        from openapi_server.models.actor_db import ActorDB
        return ActorDB(
            nombre=self._nombre,
            fecha_nacimiento=self._fecha_nacimiento,
            nacionalidad=self._nacionalidad,
            biografia=self._biografia
        )

    @classmethod
    def from_dict(cls, dikt) -> 'ActorUpdate':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ActorUpdate of this ActorUpdate.  # noqa: E501
        :rtype: ActorUpdate
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this ActorUpdate.


        :return: The id of this ActorUpdate.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this ActorUpdate.


        :param id: The id of this ActorUpdate.
        :type id: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def nombre(self) -> str:
        """Gets the nombre of this ActorUpdate.


        :return: The nombre of this ActorUpdate.
        :rtype: str
        """
        return self._nombre

    @nombre.setter
    def nombre(self, nombre: str):
        """Sets the nombre of this ActorUpdate.


        :param nombre: The nombre of this ActorUpdate.
        :type nombre: str
        """
        if nombre is None:
            raise ValueError("Invalid value for `nombre`, must not be `None`")  # noqa: E501

        self._nombre = nombre

    @property
    def fecha_nacimiento(self) -> date:
        """Gets the fecha_nacimiento of this ActorUpdate.


        :return: The fecha_nacimiento of this ActorUpdate.
        :rtype: date
        """
        return self._fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, fecha_nacimiento: date):
        """Sets the fecha_nacimiento of this ActorUpdate.


        :param fecha_nacimiento: The fecha_nacimiento of this ActorUpdate.
        :type fecha_nacimiento: date
        """
        if fecha_nacimiento is None:
            raise ValueError("Invalid value for `fecha_nacimiento`, must not be `None`")  # noqa: E501

        self._fecha_nacimiento = fecha_nacimiento

    @property
    def nacionalidad(self) -> str:
        """Gets the nacionalidad of this Actor.


        :return: The nacionalidad of this Actor.
        :rtype: str
        """
        return self._nacionalidad
    
    @nacionalidad.setter
    def nacionalidad(self, nacionalidad: str):
        """Sets the nacionalidad of this Actor.


        :param nacionalidad: The nacionalidad of this Actor.
        :type nacionalidad: str
        """
        if nacionalidad is None:
            raise ValueError("Invalid value for `nacionalidad`, must not be `None`")  # noqa: E501

        self._nacionalidad = nacionalidad

    @property
    def biografia(self) -> str:
        """Gets the biografia of this ActorUpdate.


        :return: The biografia of this ActorUpdate.
        :rtype: str
        """
        return self._biografia

    @biografia.setter
    def biografia(self, biografia: str):
        """Sets the biografia of this ActorUpdate.


        :param biografia: The biografia of this ActorUpdate.
        :type biografia: str
        """
        if biografia is None:
            raise ValueError("Invalid value for `biografia`, must not be `None`")  # noqa: E501

        self._biografia = biografia
