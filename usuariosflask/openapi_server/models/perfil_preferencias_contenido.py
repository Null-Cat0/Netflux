from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class PerfilPreferenciasContenido(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, genres=None, languages=None):  # noqa: E501
        """PerfilPreferenciasContenido - a model defined in OpenAPI

        :param genres: The genres of this PerfilPreferenciasContenido.  # noqa: E501
        :type genres: List[str]
        :param languages: The languages of this PerfilPreferenciasContenido.  # noqa: E501
        :type languages: List[str]
        """
        self.openapi_types = {
            'genres': List[str],
            'languages': List[str]
        }

        self.attribute_map = {
            'genres': 'genres',
            'languages': 'languages'
        }

        self._genres = genres
        self._languages = languages

    @classmethod
    def from_dict(cls, dikt) -> 'PerfilPreferenciasContenido':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Perfil_preferencias_contenido of this PerfilPreferenciasContenido.  # noqa: E501
        :rtype: PerfilPreferenciasContenido
        """
        return util.deserialize_model(dikt, cls)

    @property
    def genres(self) -> List[str]:
        """Gets the genres of this PerfilPreferenciasContenido.


        :return: The genres of this PerfilPreferenciasContenido.
        :rtype: List[str]
        """
        return self._genres

    @genres.setter
    def genres(self, genres: List[str]):
        """Sets the genres of this PerfilPreferenciasContenido.


        :param genres: The genres of this PerfilPreferenciasContenido.
        :type genres: List[str]
        """

        self._genres = genres

    @property
    def languages(self) -> List[str]:
        """Gets the languages of this PerfilPreferenciasContenido.


        :return: The languages of this PerfilPreferenciasContenido.
        :rtype: List[str]
        """
        return self._languages

    @languages.setter
    def languages(self, languages: List[str]):
        """Sets the languages of this PerfilPreferenciasContenido.


        :param languages: The languages of this PerfilPreferenciasContenido.
        :type languages: List[str]
        """
        allowed_values = ["Ingles", "Espanol"]  # noqa: E501
        if not set(languages).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `languages` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(languages) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._languages = languages
