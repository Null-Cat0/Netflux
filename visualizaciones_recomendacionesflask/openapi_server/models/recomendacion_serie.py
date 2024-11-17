from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util

class RecomendacionSerie(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id_perfil=None, series_recomendadas=None):  # noqa: E501
        """RecomendacionSerie - a model defined in OpenAPI

        :param id_perfil: The id_perfil of this RecomendacionSerie.  # noqa: E501
        :type id_perfil: int
        :param contenido_recomendado: The contenido_recomendado of this RecomendacionSerie.  # noqa: E501
        :type contenido_recomendado: List[Capitulo]
        """
        self.openapi_types = {
            'id_perfil': int,
            'series_recomendadas': List[str]
        }

        self.attribute_map = {
            'id_perfil': 'id_perfil',
            'series_recomendadas': 'series_recomendadas'
        }

        self._id_perfil = id_perfil
        self._series_recomendadas = series_recomendadas

    def serialize(self):
        return {
            'id_perfil': self.id_perfil,
            'series_recomendadas': self.series_recomendadas
        }

    def to_db_model(self):
        from openapi_server.models.recomendacion_serie_db import RecomendacionSerieDB
        return RecomendacionSerieDB(
            id_perfil=self.id_perfil,
            series_recomendadas=self.series_recomendadas or []
        )

    @classmethod
    def from_dict(cls, dikt) -> 'RecomendacionSerie':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The RecomendacionSerie of this RecomendacionSerie.  # noqa: E501
        :rtype: RecomendacionSerie
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id_perfil(self) -> int:
        """Gets the id_perfil of this RecomendacionSerie.


        :return: The id_perfil of this RecomendacionSerie.
        :rtype: int
        """
        return self._id_perfil

    @id_perfil.setter
    def id_perfil(self, id_perfil: int):
        """Sets the id_perfil of this RecomendacionSerie.


        :param id_perfil: The id_perfil of this RecomendacionSerie.
        :type id_perfil: int
        """

        self._id_perfil = id_perfil

    @property
    def series_recomendadas(self) -> List[str]:
        """Gets the contenido_recomendado of this RecomendacionSerie.


        :return: The contenido_recomendado of this RecomendacionSerie.
        :rtype: List[Capitulo]
        """
        return self._series_recomendadas

    @series_recomendadas.setter
    def series_recomendadas(self, series_recomendadas: List[str]):
        """Sets the contenido_recomendado of this RecomendacionSerie.


        :param contenido_recomendado: The contenido_recomendado of this RecomendacionSerie.
        :type contenido_recomendado: List[Capitulo]
        """

        self._series_recomendadas = series_recomendadas