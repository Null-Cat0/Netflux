from openapi_server import util
from openapi_server import db


class PerfilDB(db.Model):

    __tablename__ = 'perfil'

    perfil_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.user_id'))
    nombre = db.Column(db.String(255), nullable=False)
    foto_perfil = db.Column(db.String(255), nullable=True)
    # historial_vistos = db.Column(db.String(255))
    # mi_lista = db.Column(db.String(255))
    # perferencias_contenido = db.Column(db.String(255))

    def __init__(self, user_id, nombre, foto_perfil=None):  # noqa: E501
        self.user_id = user_id
        self.nombre = nombre
        self.foto_perfil = foto_perfil
        # self._historial_vistos = historial_vistos
        # self._mi_lista = mi_lista
        # self._perferencias_contenido = perferencias_contenido
    
    def to_api_model(self):
        from openapi_server.models.perfil import Perfil
        return Perfil(
            perfil_id=self.perfil_id,
            user_id=self.user_id,
            nombre=self.nombre,
            foto_perfil=self.foto_perfil,
        )
    
    