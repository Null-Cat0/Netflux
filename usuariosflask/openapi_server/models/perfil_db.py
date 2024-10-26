from openapi_server import util
from openapi_server import db

class PerfilDB(db.Model):
    """
      NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
    	Do not edit the class manually.
    """

    __tablename__ = 'perfil'

    perfil_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.user_id'))
    nombre = db.Column(db.String(255), nullable=False)
    foto_perfil = db.Column(db.String(255), nullable=True)
    # historial_vistos = db.Column(db.String(255))
    # mi_lista = db.Column(db.String(255))
    # perferencias_contenido = db.Column(db.String(255))

    def __init__(self, user_id, nombre, foto_perfil=None):  # noqa: E501
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
            'perfil_id': int,
            'user_id': int,
            'nombre': str,
            'foto_perfil': str,
            # 'historial_vistos': List[Capitulo],
            # 'mi_lista': List[Contenido],
            # 'perferencias_contenido': List[PerfilPreferenciasContenido]
        }

        self.attribute_map = {
            'perfil_id': 'perfil_id',
            'user_id': 'user_id',
            'nombre': 'nombre',
            'foto_perfil': 'foto_perfil',
            # 'historial_vistos': 'historial_vistos',
            # 'mi_lista': 'mi_lista',
            # 'perferencias_contenido': 'preferencias_contenido'
        }

        self.user_id = user_id
        self.nombre = nombre
        self.foto_perfil = foto_perfil
        # self._historial_vistos = historial_vistos
        # self._mi_lista = mi_lista
        # self._perferencias_contenido = perferencias_contenido
    
    def serialize(self):
        return {
            'perfil_id': self.perfil_id,
            'user_id': self.user_id,
            'nombre': self.nombre,
            'foto_perfil': self.foto_perfil,
        }

    @classmethod
    def from_dict(cls, dikt) -> 'PerfilDB':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Usuario of this Usuario.  # noqa: E501
        :rtype: Usuario
        """
        return util.deserialize_model(dikt, cls)