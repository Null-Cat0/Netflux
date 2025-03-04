# Se importa el fichero de configuración de los microservicios
import os, sys, requests

from openapi_server.config import ContenidosConfig as contConf
from openapi_server import db

from openapi_server.models.genero_preferencias_db import GeneroPreferenciasDB

class PreferenciasContenidoDB(db.Model):

    __tablename__ = 'preferencias_contenido'

    preferencias_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil.perfil_id'), nullable=False)
    subtitulos = db.Column(db.Boolean, nullable=False)
    idioma_audio = db.Column(db.String(255), nullable=True)

    # Lista de generos, relacion muchos a muchos con la tabla genero_preferencias
    generos = db.relationship('GeneroPreferenciasDB', backref='preferencias_contenido', cascade='all, delete')

    def __init__(self, perfil_id, subtitulos=False, idioma_audio=None):  # noqa: E501
        self.perfil_id = perfil_id
        self.subtitulos = subtitulos
        self.idioma_audio = idioma_audio

    def get_lista_generos(self):
        # Lista de los ids de los generos asociados a este perfil
        generos_ids = [genero.genero_id for genero in self.generos]

        # Ahora obtenemos los nombres de los generos asociados a este perfil con los ids obtenidos. 
        generos = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/generos")
        pref_generos = []

        for genero in generos.json():
            if genero["id"] in generos_ids:
                pref_generos.append(genero)
        return pref_generos
    
    def to_api_model(self):
        from openapi_server.models.preferencias_contenido import PreferenciasContenido
        return PreferenciasContenido(
            preferencias_id=self.preferencias_id,
            perfil_id=self.perfil_id,
            subtitulos=self.subtitulos,
            idioma_audio=self.idioma_audio,
            generos=self.get_lista_generos()
        )
