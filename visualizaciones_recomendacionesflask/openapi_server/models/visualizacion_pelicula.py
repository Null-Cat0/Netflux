from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class VisualizacionPelicula(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id_perfil=None, pelicula_id=None, fecha_visualizacion=None):  # noqa: E501
        """VisualizacionPelicula - a model defined in OpenAPI

        :param id_perfil: The id_perfil of this VisualizacionPelicula.  # noqa: E501
        :type id_perfil: int
        :param pelicula_id: The id_pelicula of this VisualizacionPelicula.  # noqa: E501
        :type pelicula_id: int
        :param fecha_visualizacion: The fecha_visualizacion of this VisualizacionPelicula.  # noqa: E501
        :type fecha_visualizacion: date
        """
        self.openapi_types = {
            'id_perfil': int,
            'pelicula_id': str,
            'fecha_visualizacion': date,
        }

        self.attribute_map = {
            'id_perfil': 'id_perfil',
            'pelicula_id': 'pelicula_id',
            'fecha_visualizacion': 'fecha_visualizacion',
        }

        self._id_perfil = id_perfil
        self._pelicula_id = pelicula_id
        self._fecha_visualizacion = fecha_visualizacion

    @classmethod
    def from_dict(cls, dikt) -> 'VisualizacionPelicula':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The VisualizacionPelicula of this Visualizacion.  # noqa: E501
        :rtype: VisualizacionPelicula
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id_perfil(self) -> int:
        """Gets the id_perfil of this VisualizacionPelicula.


        :return: The id_perfil of this VisualizacionPelicula.
        :rtype: int
        """
        return self._id_perfil

    @id_perfil.setter
    def id_perfil(self, id_perfil: int):
        """Sets the id_perfil of this VisualizacionPelicula.


        :param id_perfil: The id_perfil of this VisualizacionPelicula.
        :type id_perfil: int
        """

        self._id_perfil = id_perfil

    @property
    def pelicula_id(self) -> str:
        """Gets the pelicula_id of this VisualizacionPelicula.


        :return: The pelicula_id of this VisualizacionPelicula.
        :rtype: int
        """
        return self._pelicula_id

    @pelicula_id.setter
    def pelicula_id(self, pelicula_id: str):
        """Sets the pelicula_id of this VisualizacionPelicula.


        :param pelicula_id: The id_pelicula of this VisualizacionPelicula.
        :type pelicula_id: int
        """

        self._pelicula_id = pelicula_id 

    @property
    def fecha_visualizacion(self) -> date:
        """Gets the fecha_visualizacion of this VisualizacionPelicula.


        :return: The fecha_visualizacion of this VisualizacionPelicula.
        :rtype: date
        """
        return self._fecha_visualizacion

    @fecha_visualizacion.setter
    def fecha_visualizacion(self, fecha_visualizacion: date):
        """Sets the fecha_visualizacion of this VisualizacionPelicula.


        :param fecha_visualizacion: The fecha_visualizacion of this VisualizacionPelicula.
        :type fecha_visualizacion: date
        """

        self._fecha_visualizacion = fecha_visualizacion