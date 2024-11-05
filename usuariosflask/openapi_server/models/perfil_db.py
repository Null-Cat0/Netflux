from openapi_server import util
from openapi_server import db

from openapi_server.models.preferencias_contenido_db import PreferenciasContenidoDB


class PerfilDB(db.Model):

    __tablename__ = 'perfil'

    perfil_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.user_id'))
    nombre = db.Column(db.String(255), nullable=False)
    foto_perfil = db.Column(db.String(255), nullable=True)
    # historial_vistos = db.Column(db.String(255))
    # mi_lista = db.Column(db.String(255))
    preferencias_contenido = db.relationship('PreferenciasContenidoDB', backref='perfil', cascade='all, delete')

    def __init__(self, user_id, nombre, foto_perfil=None):  # noqa: E501
        self.user_id = user_id
        self.nombre = nombre
        self.foto_perfil = foto_perfil
        # self._historial_vistos = historial_vistos
        # self._mi_lista = mi_lista
        # self._perferencias_contenido = perferencias_contenido

    def get_preferencias_contenido(self):
        from openapi_server.models.preferencias_contenido import PreferenciasContenido

        # Primero obtenemos el objeto PreferenciasContenidoDB asociado a este perfil
        preferencias_db = PreferenciasContenidoDB.query.filter_by(perfil_id=self.perfil_id).first()

        if preferencias_db is None:
            return None

        # Ahora obtenemos los generos asociados a este perfil
        generos = preferencias_db.get_lista_generos()

        # Creamos el objeto PreferenciasContenido
        preferencias_api = PreferenciasContenido(
            perfil_id=preferencias_db.perfil_id,
            subtitulos=preferencias_db.subtitulos,
            idioma_audio=preferencias_db.idioma_audio,
            generos=generos
        )

        return preferencias_api
    
    def to_api_model(self):
        from openapi_server.models.perfil import Perfil
        return Perfil(
            perfil_id=self.perfil_id,
            user_id=self.user_id,
            nombre=self.nombre,
            foto_perfil=self.foto_perfil,
            preferencias_contenido=self.get_preferencias_contenido()
        )