from openapi_server import util

from openapi_server.models.actor import Actor
from openapi_server.models.genero import Genero
from openapi_server.models.base_model import Model

from typing import List
from bson import ObjectId

class PeliculaUpdate(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, titulo=None, genero=None, sinopsis=None, anio_estreno=None, duracion=None, actores=None):  # noqa: E501
        """PeliculaUpdate - a model defined in OpenAPI

        :param id: The id of this PeliculaUpdate.  # noqa: E501
        :type id: int
        :param titulo: The titulo of this PeliculaUpdate.  # noqa: E501
        :type titulo: str
        :param genero: The genero of this PeliculaUpdate.  # noqa: E501
        :type genero: str
        :param sinopsis: The sinopsis of this PeliculaUpdate.  # noqa: E501
        :type sinopsis: str
        :param anio_estreno: The anio_estreno of this PeliculaUpdate.  # noqa: E501
        :type anio_estreno: int
        :param duracion: The duracion of this PeliculaUpdate.  # noqa: E501
        :type duracion: int
        :param temporadas: The temporadas of this PeliculaUpdate.  # noqa: E501
        :type temporadas: List[Temporada]
        :param actores: The actores of this PeliculaUpdate.  # noqa: E501
        :type actores: List[Actor]
        """
        self.openapi_types = {
            'id': int,
            'titulo': str,
            'genero': List[str],
            'sinopsis': str,
            'anio_estreno': int,
            'duracion': int,
            'actores': List[str],
        }

        self.attribute_map = {
            'id': 'id',
            'titulo': 'titulo',
            'genero': 'genero',
            'sinopsis': 'sinopsis',
            'anio_estreno': 'anio_estreno',
            'duracion': 'duracion',
            'actores': 'actores',
        }

        self._id = id
        self._titulo = titulo
        self._genero = [ObjectId(genero) if isinstance(genero, str) else genero for genero in (genero or [])]
        self._sinopsis = sinopsis
        self._anio_estreno = anio_estreno
        self._duracion = duracion
        self._actores = [ObjectId(actor) if isinstance(actor, str) else actor for actor in (actores or [])]


    def to_db_model(self):
        from openapi_server.models.pelicula_db import PeliculaDB
        return PeliculaDB(
            titulo=self._titulo,
            genero=[ObjectId(genero) for genero in self._genero] if self._genero else [],
            sinopsis=self._sinopsis,
            anio_estreno=self._anio_estreno,
            duracion=self._duracion,
            actores=[ObjectId(actor) for actor in self._actores] if self._actores else [],
        )

    @classmethod
    def from_dict(cls, dikt) -> 'PeliculaUpdate':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PeliculaUpdate of this PeliculaUpdate.  # noqa: E501
        :rtype: PeliculaUpdate
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this PeliculaUpdate.


        :return: The id of this PeliculaUpdate.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this PeliculaUpdate.


        :param id: The id of this PeliculaUpdate.
        :type id: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def titulo(self) -> str:
        """Gets the titulo of this PeliculaUpdate.


        :return: The titulo of this PeliculaUpdate.
        :rtype: str
        """
        return self._titulo

    @titulo.setter
    def titulo(self, titulo: str):
        """Sets the titulo of this PeliculaUpdate.


        :param titulo: The titulo of this PeliculaUpdate.
        :type titulo: str
        """
        if titulo is None:
            raise ValueError("Invalid value for `titulo`, must not be `None`")  # noqa: E501

        self._titulo = titulo

    @property
    def genero(self) -> List[Genero]:
        """Gets the genero of this PeliculaUpdate.


        :return: The genero of this PeliculaUpdate.
        :rtype: str
        """
        return self._genero

    @genero.setter
    def genero(self, genero: List[Genero]):
        """Sets the genero of this PeliculaUpdate.


        :param genero: The genero of this PeliculaUpdate.
        :type genero: str
        """
        if genero is None:
            raise ValueError("Invalid value for `genero`, must not be `None`")  # noqa: E501

        self._genero = genero

    @property
    def sinopsis(self) -> str:
        """Gets the sinopsis of this PeliculaUpdate.


        :return: The sinopsis of this PeliculaUpdate.
        :rtype: str
        """
        return self._sinopsis

    @sinopsis.setter
    def sinopsis(self, sinopsis: str):
        """Sets the sinopsis of this PeliculaUpdate.


        :param sinopsis: The sinopsis of this PeliculaUpdate.
        :type sinopsis: str
        """
        if sinopsis is None:
            raise ValueError("Invalid value for `sinopsis`, must not be `None`")  # noqa: E501

        self._sinopsis = sinopsis

    @property
    def anio_estreno(self) -> int:
        """Gets the anio_estreno of this PeliculaUpdate.


        :return: The anio_estreno of this PeliculaUpdate.
        :rtype: int
        """
        return self._anio_estreno

    @anio_estreno.setter
    def anio_estreno(self, anio_estreno: int):
        """Sets the anio_estreno of this PeliculaUpdate.


        :param anio_estreno: The anio_estreno of this PeliculaUpdate.
        :type anio_estreno: int
        """
        if anio_estreno is None:
            raise ValueError("Invalid value for `anio_estreno`, must not be `None`")  # noqa: E501

        self._anio_estreno = anio_estreno

    @property
    def duracion(self) -> int:
        """Gets the duracion of this PeliculaUpdate.


        :return: The duracion of this PeliculaUpdate.
        :rtype: int
        """
        return self._duracion

    @duracion.setter
    def duracion(self, duracion: int):
        """Sets the duracion of this PeliculaUpdate.


        :param duracion: The duracion of this PeliculaUpdate.
        :type duracion: int
        """

        self._duracion = duracion

    @property
    def actores(self) -> List[Actor]:
        """Gets the actores of this PeliculaUpdate.


        :return: The actores of this PeliculaUpdate.
        :rtype: List[Actor]
        """
        return self._actores

    @actores.setter
    def actores(self, actores: List[Actor]):
        """Sets the actores of this PeliculaUpdate.


        :param actores: The actores of this PeliculaUpdate.
        :type actores: List[Actor]
        """

        self._actores = actores    
