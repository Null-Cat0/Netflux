from datetime import date, datetime  # noqa: F401

from typing import List, Dict

from openapi_server.models.base_model import Model
from openapi_server.models.perfil import Perfil  # noqa: E501

from openapi_server import util
from openapi_server import db

class Usuario(db.Model):
    """
      NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
    	Do not edit the class manually.
    """

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    correo_electronico = db.Column(db.String(255))
    password = db.Column(db.String(255))
    pais = db.Column(db.String(255))
    plan_suscripcion = db.Column(db.String(255))
    dispositivos = db.Column(db.String(255))
    #perfiles = db.relationship('Perfil', backref='usuario', lazy=True)

    def __init__(self, nombre, correo_electronico, password, pais, plan_suscripcion, dispositivos):  # noqa: E501
        """Usuario - a model defined in OpenAPI

        :param id: The id of this Usuario.  # noqa: E501
        :type id: int
        :param nombre: The nombre of this Usuario.  # noqa: E501
        :type nombre: str
        :param correo_electronico: The correo_electronico of this Usuario.  # noqa: E501
        :type correo_electronico: str
        :param pais: The pais of this Usuario.  # noqa: E501
        :type pais: str
        :param plan_suscripcion: The plan_suscripcion of this Usuario.  # noqa: E501
        :type plan_suscripcion: str
        :param dispositivos: The dispositivos of this Usuario.  # noqa: E501
        :type dispositivos: List[str]
        :param perfiles: The perfiles of this Usuario.  # noqa: E501
        :type perfiles: List[Perfil]
        """
        self.openapi_types = {
            'user_id': int,
            'nombre': str,
            'correo_electronico': str,
            'password': str,
            'pais': str,
            'plan_suscripcion': str,
            'dispositivos': List[str],
            'perfiles': List[Perfil]
        }

        self.attribute_map = {
            'user_id': 'user_id',
            'nombre': 'nombre',
            'correo_electronico': 'correo_electronico',
            'password': str,
            'pais': 'pais',
            'plan_suscripcion': 'plan_suscripcion',
            'dispositivos': 'dispositivos',
            'perfiles': 'perfiles'
        }

        self.nombre = nombre
        self.correo_electronico = correo_electronico
        self.password = password
        self.pais = pais
        self.plan_suscripcion = plan_suscripcion
        self.dispositivos = dispositivos
        # self.perfiles = perfiles
    
    def serialize(self):
        return {
            'user_id': self.user_id,
            'nombre': self.nombre,
            'correo_electronico': self.correo_electronico,
            'pais': self.pais,
            'plan_suscripcion': self.plan_suscripcion,
            'dispositivos': self.dispositivos
        }

    @classmethod
    def from_dict(cls, dikt) -> 'Usuario':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Usuario of this Usuario.  # noqa: E501
        :rtype: Usuario
        """
        return util.deserialize_model(dikt, cls)

    # @property
    # def id(self) -> int:
    #     """Gets the id of this Usuario.
    #
    #
    #     :return: The id of this Usuario.
    #     :rtype: int
    #     """
    #     return self._id
    #
    # @id.setter
    # def id(self, id: int):
    #     """Sets the id of this Usuario.
    #
    #
    #     :param id: The id of this Usuario.
    #     :type id: int
    #     """
    #
    #     self._id = id
    #
    # @property
    # def nombre(self) -> str:
    #     """Gets the nombre of this Usuario.
    #
    #
    #     :return: The nombre of this Usuario.
    #     :rtype: str
    #     """
    #     return self._nombre
    #
    # @nombre.setter
    # def nombre(self, nombre: str):
    #     """Sets the nombre of this Usuario.
    #
    #
    #     :param nombre: The nombre of this Usuario.
    #     :type nombre: str
    #     """
    #     if nombre is None:
    #         raise ValueError("Invalid value for `nombre`, must not be `None`")  # noqa: E501
    #
    #     self._nombre = nombre
    #
    # @property
    # def correo_electronico(self) -> str:
    #     """Gets the correo_electronico of this Usuario.
    #
    #
    #     :return: The correo_electronico of this Usuario.
    #     :rtype: str
    #     """
    #     return self._correo_electronico
    #
    # @correo_electronico.setter
    # def correo_electronico(self, correo_electronico: str):
    #     """Sets the correo_electronico of this Usuario.
    #
    #
    #     :param correo_electronico: The correo_electronico of this Usuario.
    #     :type correo_electronico: str
    #     """
    #     if correo_electronico is None:
    #         raise ValueError("Invalid value for `correo_electronico`, must not be `None`")  # noqa: E501
    #
    #     self._correo_electronico = correo_electronico
    #
    # @property
    # def pais(self) -> str:
    #     """Gets the pais of this Usuario.
    #
    #
    #     :return: The pais of this Usuario.
    #     :rtype: str
    #     """
    #     return self._pais
    #
    # @pais.setter
    # def pais(self, pais: str):
    #     """Sets the pais of this Usuario.
    #
    #
    #     :param pais: The pais of this Usuario.
    #     :type pais: str
    #     """
    #
    #     self._pais = pais
    #
    # @property
    # def plan_suscripcion(self) -> str:
    #     """Gets the plan_suscripcion of this Usuario.
    #
    #
    #     :return: The plan_suscripcion of this Usuario.
    #     :rtype: str
    #     """
    #     return self._plan_suscripcion
    #
    # @plan_suscripcion.setter
    # def plan_suscripcion(self, plan_suscripcion: str):
    #     """Sets the plan_suscripcion of this Usuario.
    #
    #
    #     :param plan_suscripcion: The plan_suscripcion of this Usuario.
    #     :type plan_suscripcion: str
    #     """
    #     allowed_values = ["Basico", "Estandar", "Premium"]  # noqa: E501
    #     if plan_suscripcion not in allowed_values:
    #         raise ValueError(
    #             "Invalid value for `plan_suscripcion` ({0}), must be one of {1}"
    #             .format(plan_suscripcion, allowed_values)
    #         )
    #
    #     self._plan_suscripcion = plan_suscripcion
    #
    # @property
    # def dispositivos(self) -> List[str]:
    #     """Gets the dispositivos of this Usuario.
    #
    #
    #     :return: The dispositivos of this Usuario.
    #     :rtype: List[str]
    #     """
    #     return self._dispositivos
    #
    # @dispositivos.setter
    # def dispositivos(self, dispositivos: List[str]):
    #     """Sets the dispositivos of this Usuario.
    #
    #
    #     :param dispositivos: The dispositivos of this Usuario.
    #     :type dispositivos: List[str]
    #     """
    #
    #     self._dispositivos = dispositivos
    #
    # @property
    # def perfiles(self) -> List[Perfil]:
    #     """Gets the perfiles of this Usuario.
    #
    #
    #     :return: The perfiles of this Usuario.
    #     :rtype: List[Perfil]
    #     """
    #     return self._perfiles
    #
    # @perfiles.setter
    # def perfiles(self, perfiles: List[Perfil]):
    #     """Sets the perfiles of this Usuario.
    #
    #
    #     :param perfiles: The perfiles of this Usuario.
    #     :type perfiles: List[Perfil]
    #     """
    #
    #     self._perfiles = perfiles
