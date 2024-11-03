from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class PreferenciasContenido(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, perfil_id, subtitulos=False, idioma_audio=None, generos=None):  # noqa: E501
        """PreferenciasContenido - a model defined in OpenAPI

        :param perfil_id: The perfil_id of this PreferenciasContenido.  # noqa: E501
        :type perfil_id: int
        :param subtitulos: The subtitulos of this PreferenciasContenido.  # noqa: E501
        :type subtitulos: bool
        :param idioma_audio: The idioma_audio of this PreferenciasContenido.  # noqa: E501
        :type idioma_audio: str
        :param generos: The generos of this PreferenciasContenido.  # noqa: E501
        :type generos: List[str]
        """
        self.openapi_types = {
            'perfil_id': int,
            'subtitulos': bool,
            'idioma_audio': str,
            'generos': List[str],
        }

        self.attribute_map = {
            'perfil_id': 'perfil_id',
            'subtitulos': 'subtitulos',
            'idioma_audio': 'idioma_audio',
            'generos': 'generos',
        }

        self._perfil_id = perfil_id
        self._subtitulos = subtitulos
        self._idioma_audio = idioma_audio
        self._generos = generos

    def serialize(self):
        return {
            'perfil_id': self._perfil_id,
            'subtitulos': self._subtitulos,
            'idioma_audio': self._idioma_audio,
            'generos': self._generos
        }

    def to_db_model(self):
        from openapi_server.models.preferencias_contenido_db import PreferenciasContenidoDB
        return PreferenciasContenidoDB(
            perfil_id=self._perfil_id,
            subtitulos=self._subtitulos,
            idioma_audio=self._idioma_audio,
        )

    @classmethod
    def from_dict(cls, dikt) -> 'PreferenciasContenido':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Perfil_preferencias_contenido of this PreferenciasContenido.  # noqa: E501
        :rtype: PreferenciasContenido
        """
        return util.deserialize_model(dikt, cls)

    @property
    def subtitulos(self) -> bool:
        """Gets the subtitulos of this PreferenciasContenido.

        :return: The subtitulos of this PreferenciasContenido.
bool        :rtype: bool
        """
        return self._subtitulos

    @subtitulos.setter
    def subtitulos(self, subtitulos: bool):
        """Sets the subtitulos of this PreferenciasContenido.

        :param subtitulos: The subtitulos of this PreferenciasContenido.
        :type subtitulos: bool
        """
        if subtitulos is None:
            raise ValueError("Invalid value for `subtitulos`, must not be `None`")
        
        self._subtitulos = subtitulos

    @property
    def idioma_audio(self) -> str:
        """Gets the idioma_audio of this PreferenciasContenido.

        :return: The idioma_audio of this PreferenciasContenido.
        :rtype: str
        """
        return self._idioma_audio

    @idioma_audio.setter
    def idioma_audio(self, idioma_audio: str):
        """Sets the idioma_audio of this PreferenciasContenido.

        :param idioma_audio: The idioma_audio of this PreferenciasContenido.
        :type idioma_audio: str
        """
        # Should be revisited to limit the possible values
        self._idioma_audio = idioma_audio

    @property
    def perfil_id(self) -> int:
        """Gets the perfil_id of this PreferenciasContenido.

        :return: The perfil_id of this PreferenciasContenido.
        :rtype: int
        """
        return self._perfil_id

    @perfil_id.setter
    def perfil_id(self, perfil_id: int):
        """Sets the perfil_id of this PreferenciasContenido.

        :param perfil_id: The perfil_id of this PreferenciasContenido.
        :type perfil_id: int
        """
        if perfil_id is None:
            raise ValueError("Invalid value for `perfil_id`, must not be `None`")

        self._perfil_id = perfil_id

    @property
    def generos(self) -> List[str]:
        """Gets the generos of this PreferenciasContenido.


        :return: The generos of this PreferenciasContenido.
        :rtype: List[str]
        """
        return self._generos

    @generos.setter
    def generos(self, generos: List[str]):
        """Sets the generos of this PreferenciasContenido.


        :param generos: The generos of this PreferenciasContenido.
        :type generos: List[str]
        """
        self._generos = generos