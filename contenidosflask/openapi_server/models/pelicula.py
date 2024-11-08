from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server.models.actor import Actor
from openapi_server import util
from bson import ObjectId


class Pelicula(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, titulo=None, genero=None, sinopsis=None, anio_estreno=None, duracion=None, actores=None, secuela=None, precuela=None):  # noqa: E501
        """Pelicula - a model defined in OpenAPI

        :param id: The id of this Pelicula.  # noqa: E501
        :type id: int
        :param titulo: The titulo of this Pelicula.  # noqa: E501
        :type titulo: str
        :param genero: The genero of this Pelicula.  # noqa: E501
        :type genero: str
        :param sinopsis: The sinopsis of this Pelicula.  # noqa: E501
        :type sinopsis: str
        :param anio_estreno: The anio_estreno of this Pelicula.  # noqa: E501
        :type anio_estreno: int
        :param duracion: The duracion of this Pelicula.  # noqa: E501
        :type duracion: int
        :param actores: The actores of this Pelicula.  # noqa: E501
        :type actores: List[Actor]
        """
        self.openapi_types = {
            'id': str,
            'titulo': str,
            'genero': List[str],
            'sinopsis': str,
            'anio_estreno': int,
            'duracion': int,
            'actores': List[str],

            'secuela': str,
            'precuela': str
        }

        self.attribute_map = {
            'id': 'id',
            'titulo': 'titulo',
            'genero': 'genero',
            'sinopsis': 'sinopsis',
            'anio_estreno': 'anio_estreno',
            'duracion': 'duracion',
            'actores': 'actores',

            'secuela': 'secuela',
            'precuela': 'precuela'
        }

        self._id = id
        self._titulo = titulo
        self._genero = genero
        self._sinopsis = sinopsis
        self._anio_estreno = anio_estreno
        self._duracion = duracion
        self._actores = [ObjectId(actor) if isinstance(actor, str) else actor for actor in (actores or [])]
        self._secuela = secuela if isinstance(secuela, str) else secuela
        self._precuela = precuela if isinstance(precuela, str) else precuela
        
    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "sinopsis": self.sinopsis,
            "anio_estreno": self.anio_estreno,
            "duracion": self.duracion,
            "actores": [actor.serialize() for actor in self.actores] if self.actores else [],

            "secuela": self.secuela,
            "precuela": self.precuela
        }

    def to_db_model(self):
        from openapi_server.models.pelicula_db import PeliculaDB
        return PeliculaDB(
            titulo=self._titulo,
            genero=self._genero,
            sinopsis=self._sinopsis,
            anio_estreno=self._anio_estreno,
            duracion=self._duracion,
            actores=[ObjectId(actor) for actor in self._actores],

            secuela=ObjectId(self._secuela) if self._secuela else None,
            precuela=ObjectId(self._precuela) if self._precuela else None
        )

    @classmethod
    def from_dict(cls, dikt) -> 'Pelicula':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Pelicula of this Pelicula.  # noqa: E501
        :rtype: Pelicula
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Pelicula.


        :return: The id of this Pelicula.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Pelicula.


        :param id: The id of this Pelicula.
        :type id: int
        """

        self._id = id

    @property
    def titulo(self) -> str:
        """Gets the titulo of this Pelicula.


        :return: The titulo of this Pelicula.
        :rtype: str
        """
        return self._titulo

    @titulo.setter
    def titulo(self, titulo: str):
        """Sets the titulo of this Pelicula.


        :param titulo: The titulo of this Pelicula.
        :type titulo: str
        """
        if titulo is None:
            raise ValueError("Invalid value for `titulo`, must not be `None`")  # noqa: E501

        self._titulo = titulo

    @property
    def genero(self) -> List[str]:
        """Gets the genero of this Pelicula.


        :return: The genero of this Pelicula.
        :rtype: str
        """
        return self._genero

    @genero.setter
    def genero(self, genero: List[str]):
        """Sets the genero of this Pelicula.


        :param genero: The genero of this Pelicula.
        :type genero: str
        """
        if genero is None:
            raise ValueError("Invalid value for `genero`, must not be `None`")  # noqa: E501

        self._genero = genero

    @property
    def sinopsis(self) -> str:
        """Gets the sinopsis of this Pelicula.


        :return: The sinopsis of this Pelicula.
        :rtype: str
        """
        return self._sinopsis

    @sinopsis.setter
    def sinopsis(self, sinopsis: str):
        """Sets the sinopsis of this Pelicula.


        :param sinopsis: The sinopsis of this Pelicula.
        :type sinopsis: str
        """
        if sinopsis is None:
            raise ValueError("Invalid value for `sinopsis`, must not be `None`")  # noqa: E501

        self._sinopsis = sinopsis

    @property
    def anio_estreno(self) -> int:
        """Gets the anio_estreno of this Pelicula.


        :return: The anio_estreno of this Pelicula.
        :rtype: int
        """
        return self._anio_estreno

    @anio_estreno.setter
    def anio_estreno(self, anio_estreno: int):
        """Sets the anio_estreno of this Pelicula.


        :param anio_estreno: The anio_estreno of this Pelicula.
        :type anio_estreno: int
        """
        if anio_estreno is None:
            raise ValueError("Invalid value for `anio_estreno`, must not be `None`")  # noqa: E501

        self._anio_estreno = anio_estreno

    @property
    def duracion(self) -> int:
        """Gets the duracion of this Pelicula.


        :return: The duracion of this Pelicula.
        :rtype: int
        """
        return self._duracion

    @duracion.setter
    def duracion(self, duracion: int):
        """Sets the duracion of this Pelicula.


        :param duracion: The duracion of this Pelicula.
        :type duracion: int
        """

        self._duracion = duracion

    @property
    def actores(self) -> List[Actor]:
        """Gets the actores of this Pelicula.


        :return: The actores of this Pelicula.
        :rtype: List[Actor]
        """
        return self._actores

    @actores.setter
    def actores(self, actores: List[Actor]):
        """Sets the actores of this Pelicula.


        :param actores: The actores of this Pelicula.
        :type actores: List[Actor]
        """

        self._actores = actores

    @property
    def secuela(self) -> {str, str}:
        """Gets the secuela of this Pelicula.


        :return: The secuela of this Pelicula.
        :rtype: str
        """
        return self._secuela

    @secuela.setter
    def secuela(self, secuela: {str, str}):
        """Sets the secuela of this Pelicula.


        :param secuela: The secuela of this Pelicula.
        :type secuela: str
        """

        self._secuela = secuela

    @property
    def precuela(self) -> {str, str}:
        """Gets the precuela of this Pelicula.


        :return: The precuela of this Pelicula.
        :rtype: str
        """
        return self._precuela

    @precuela.setter
    def precuela(self, precuela: {str, str}):
        """Sets the precuela of this Pelicula.


        :param precuela: The precuela of this Pelicula.
        :type precuela: str
        """

        self._precuela = precuela