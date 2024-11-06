from datetime import date, datetime  # noqa: F401

from typing import List  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server.models.actor import Actor  # noqa: E501
from openapi_server import util
from bson import ObjectId

class CapituloEmbedded(Model):
    def __init__(self, numero=None, titulo=None, duracion=None, sinopsis=None):
        self.openapi_types = {
            'numero': int,
            'titulo': str,
            'duracion': int,
            'sinopsis': str
        }
        self.attribute_map = {
            'numero': 'numero',
            'titulo': 'titulo',
            'duracion': 'duracion',
            'sinopsis': 'sinopsis'
        }
        self._numero = numero
        self._titulo = titulo
        self._duracion = duracion
        self._sinopsis = sinopsis
    
    @property
    def numero(self):
        return self._numero

    @property
    def titulo(self):
        return self._titulo

    @property
    def duracion(self):
        return self._duracion

    @property
    def sinopsis(self):
        return self._sinopsis
    
    def serialize(self):
        return {
            "numero": self.numero,
            "titulo": self.titulo,
            "duracion": self.duracion,
            "sinopsis": self.sinopsis
        }

    def to_db_model(self):
        from openapi_server.models.serie_db import CapituloEmbeddedDB
        return CapituloEmbeddedDB(
            numero=self._numero,
            titulo=self._titulo,
            duracion=self._duracion,
            sinopsis=self._sinopsis
        )

class TemporadaEmbedded(Model):
    def __init__(self, numero=None, anio_lanzamiento=None, capitulos=None):
        self.openapi_types = {
            'numero': int,
            'anio_lanzamiento': int,
            'capitulos': List[CapituloEmbedded]
        }
        self.attribute_map = {
            'numero': 'numero',
            'anio_lanzamiento': 'anioLanzamiento',
            'capitulos': 'capitulos'
        }
        self._numero = numero
        self._anio_lanzamiento = anio_lanzamiento
        self._capitulos = [
            CapituloEmbedded(**capitulo) if isinstance(capitulo, dict) else capitulo
            for capitulo in (capitulos or [])
        ]
    
    @property
    def numero(self):
        return self._numero

    @numero.setter
    def id(self, numero: int):
        """Sets the id of this Serie.


        :param id: The id of this Serie.
        :type id: int
        """

        self._numero = numero

    @property
    def anio_lanzamiento(self):
        return self._anio_lanzamiento

    @property
    def capitulos(self):
        return self._capitulos
    
    def serialize(self):
        return {
            "numero": self.numero,
            "anio_lanzamiento": self.anio_lanzamiento,
            "capitulos": [capitulo.serialize() for capitulo in self.capitulos]
        }

    def to_db_model(self):
        from openapi_server.models.serie_db import TemporadaEmbeddedDB
        return TemporadaEmbeddedDB(
            numero=self._numero,
            anio_lanzamiento=self._anio_lanzamiento,
            capitulos=[capitulo.to_db_model() for capitulo in self.capitulos]
        )


class Serie(Model):
    def __init__(self, id=None, titulo=None, genero=None, sinopsis=None, anio_estreno=None, temporadas=None, actores=None):
        self.openapi_types = {
            'id': str,
            'titulo': str,
            'genero': str,
            'sinopsis': str,
            'anio_estreno': int,
            'temporadas': List[TemporadaEmbedded],
            'actores': List[Actor]
        }
        self.attribute_map = {
            'id': 'id',
            'titulo': 'titulo',
            'genero': 'genero',
            'sinopsis': 'sinopsis',
            'anio_estreno': 'anio_estreno',
            'temporadas': 'temporadas',
            'actores': 'actores'
        }
        self._id = id
        self._titulo = titulo
        self._genero = genero
        self._sinopsis = sinopsis
        self._anio_estreno = anio_estreno
        
        self._temporadas = [
            TemporadaEmbedded(**temporada) if isinstance(temporada, dict) else temporada
            for temporada in (temporadas or [])
        ]
        
        # Convertir los actores en una lista de ObjectIds si no lo están ya
        self._actores = [ObjectId(actor) if isinstance(actor, str) else actor for actor in (actores or [])]
    

    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "sinopsis": self.sinopsis,
            "anio_estreno": self.anio_estreno,
            "temporadas": [temporada.serialize() for temporada in self.temporadas],
            "actores": [actor.serialize() for actor in self.actores] if self.actores else []
        }

    def to_db_model(self):
        from openapi_server.models.serie_db import SerieDB
        return SerieDB(
            titulo=self._titulo,
            genero=self._genero,
            sinopsis=self._sinopsis,
            anio_estreno=self._anio_estreno,
            temporadas=[temporada.to_db_model() for temporada in self._temporadas],
            actores=[ObjectId(id) for id in self._actores] if self._actores else []
        )


    @classmethod
    def from_dict(cls, dikt) -> 'Serie':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Serie of this Serie.  # noqa: E501
        :rtype: Serie
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Serie.


        :return: The id of this Serie.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Serie.


        :param id: The id of this Serie.
        :type id: int
        """

        self._id = id

    @property
    def titulo(self) -> str:
        """Gets the titulo of this Serie.


        :return: The titulo of this Serie.
        :rtype: str
        """
        return self._titulo

    @titulo.setter
    def titulo(self, titulo: str):
        """Sets the titulo of this Serie.


        :param titulo: The titulo of this Serie.
        :type titulo: str
        """
        if titulo is None:
            raise ValueError("Invalid value for `titulo`, must not be `None`")  # noqa: E501

        self._titulo = titulo

    @property
    def genero(self) -> str:
        """Gets the genero of this Serie.


        :return: The genero of this Serie.
        :rtype: str
        """
        return self._genero

    @genero.setter
    def genero(self, genero: str):
        """Sets the genero of this Serie.


        :param genero: The genero of this Serie.
        :type genero: str
        """
        if genero is None:
            raise ValueError("Invalid value for `genero`, must not be `None`")  # noqa: E501

        self._genero = genero

    @property
    def sinopsis(self) -> str:
        """Gets the sinopsis of this Serie.


        :return: The sinopsis of this Serie.
        :rtype: str
        """
        return self._sinopsis

    @sinopsis.setter
    def sinopsis(self, sinopsis: str):
        """Sets the sinopsis of this Serie.


        :param sinopsis: The sinopsis of this Serie.
        :type sinopsis: str
        """
        if sinopsis is None:
            raise ValueError("Invalid value for `sinopsis`, must not be `None`")  # noqa: E501

        self._sinopsis = sinopsis

    @property
    def anio_estreno(self) -> int:
        """Gets the anio_estreno of this Serie.


        :return: The anio_estreno of this Serie.
        :rtype: int
        """
        return self._anio_estreno

    @anio_estreno.setter
    def anio_estreno(self, anio_estreno: int):
        """Sets the anio_estreno of this Serie.


        :param anio_estreno: The anio_estreno of this Serie.
        :type anio_estreno: int
        """
        if anio_estreno is None:
            raise ValueError("Invalid value for `anio_estreno`, must not be `None`")  # noqa: E501

        self._anio_estreno = anio_estreno

    @property
    def temporadas(self) -> List[TemporadaEmbedded]:
        """Gets the temporadas of this Serie.


        :return: The temporadas of this Serie.
        :rtype: List[Temporada]
        """
        return self._temporadas

    @temporadas.setter
    def temporadas(self, temporadas: List[TemporadaEmbedded]):
        """Sets the temporadas of this Serie.


        :param temporadas: The temporadas of this Serie.
        :type temporadas: List[Temporada]
        """

        self._temporadas = temporadas

    @property
    def actores(self) -> List[Actor]:
        """Gets the actores of this Serie.


        :return: The actores of this Serie.
        :rtype: List[Actor]
        """
        return self._actores

    @actores.setter
    def actores(self, actores: List[Actor]):
        """Sets the actores of this Serie.


        :param actores: The actores of this Serie.
        :type actores: List[Actor]
        """

        self._actores = actores
