from openapi_server import util
from openapi_server import db

from openapi_server.models.genero_db import GeneroDB
from openapi_server.models.genero_preferencias_db import GeneroPreferenciasDB

class PreferenciasContenidoDB(db.Model):

    __tablename__ = 'preferencias_contenido'

    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil.perfil_id'), nullable=False, primary_key=True)
    subtitulos = db.Column(db.Boolean, nullable=False)
    idioma_audio = db.Column(db.String(255), nullable=False)

    # Lista de generos, relacion muchos a muchos con la tabla genero_preferencias
    generos = db.relationship('GeneroPreferenciasDB', backref='preferencias_contenido', cascade='all, delete')

    def __init__(self, perfil_id, subtitulos=False, idioma_audio=None):  # noqa: E501
        self.perfil_id = perfil_id
        self.subtitulos = subtitulos
        self.idioma_audio = idioma_audio

    def get_lista_generos(self):
        # Lista de los ids de los generos asociados a este perfil
        generos_ids = [genero.genero_id for genero in self.generos]

        # Ahora obtenemos los nombres de los generos asociados a este perfil con los ids obtenidos
        generos = GeneroDB.query.filter(GeneroDB.genero_id.in_(generos_ids)).all()
        nombre_generos = [genero.nombre for genero in generos]
        return nombre_generos
    
    def to_api_model(self):
        from openapi_server.models.preferencias_contenido import PreferenciasContenido
        return PreferenciasContenido(
            perfil_id=self.perfil_id,
            subtitulos=self.subtitulos,
            idioma_audio=self.idioma_audio,
            generos=get_lista_generos()
        )