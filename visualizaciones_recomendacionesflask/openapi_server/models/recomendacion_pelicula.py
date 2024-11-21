from openapi_server import util
from openapi_server.models.base_model import Model

from typing import List

class RecomendacionPelicula(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id_perfil=None, peliculas_recomendadas=None):  # noqa: E501
        """RecomendacionPelicula - a model defined in OpenAPI

        :param id_perfil: The id_perfil of this RecomendacionPelicula.  # noqa: E501
        :type id_perfil: int
        :param peliculas_recomendadas: The peliculas_recomendadas of this RecomendacionPelicula.  # noqa: E501
        :type peliculas_recomendadas: List[str]
        """
        self.openapi_types = {
            'id_perfil': int,
            'peliculas_recomendadas': List[str]
        }

        self.attribute_map = {
            'id_perfil': 'id_perfil',
            'peliculas_recomendadas': 'peliculas_recomendadas'
        }

        self._id_perfil = id_perfil
        self._peliculas_recomendadas = peliculas_recomendadas

    def serialize(self):
        return {
            'id_perfil': self.id_perfil,
            'peliculas_recomendadas': self.peliculas_recomendadas
        }

    def to_db_model(self):
        from openapi_server.models.recomendacion_pelicula_db import RecomendacionPeliculaDB
        return RecomendacionPeliculaDB(
            id_perfil=self.id_perfil,
            peliculas_recomendadas=self.peliculas_recomendadas or []
        )

    @classmethod
    def from_dict(cls, dikt) -> 'RecomendacionPelicula':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The RecomendacionPelicula of this RecomendacionPelicula.  # noqa: E501
        :rtype: RecomendacionPelicula
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id_perfil(self) -> int:
        """Gets the id_perfil of this RecomendacionPelicula.


        :return: The id_perfil of this RecomendacionPelicula.
        :rtype: int
        """
        return self._id_perfil

    @id_perfil.setter
    def id_perfil(self, id_perfil: int):
        """Sets the id_perfil of this RecomendacionPelicula.


        :param id_perfil: The id_perfil of this RecomendacionPelicula.
        :type id_perfil: int
        """

        self._id_perfil = id_perfil

    @property
    def peliculas_recomendadas(self) -> List[str]:
        """Gets the peliculas_recomendadas of this RecomendacionPelicula.


        :return: The peliculas_recomendadas of this RecomendacionPelicula.
        :rtype: List[Pelicula]
        """
        return self._peliculas_recomendadas

    @peliculas_recomendadas.setter
    def peliculas_recomendadas(self, peliculas_recomendadas: List[str]):
        """Sets the peliculas_recomendadas of this RecomendacionPelicula.


        :param peliculas_recomendadas: The peliculas_recomendadas of this RecomendacionPelicula.
        :type peliculas_recomendadas: List[Pelicula]
        """

        self._peliculas_recomendadas = peliculas_recomendadas
