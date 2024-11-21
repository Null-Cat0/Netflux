# Se importa el fichero de configuración de los microservicios
import os, sys, requests
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(app_path)

from global_config import ContenidosConfig as contConf

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
        # Para ello, realizamos una petición al microservicio de contenidos
        response_generos = requests.get(f'{contConf.CONTENIDOS_BASE_URL}/obtener_lista_generos', json=generos_ids)
        if response_generos.status_code == 200:
            return response_generos.json()
        else:
            return []
    
    def to_api_model(self):
        from openapi_server.models.preferencias_contenido import PreferenciasContenido
        return PreferenciasContenido(
            preferencias_id=self.preferencias_id,
            perfil_id=self.perfil_id,
            subtitulos=self.subtitulos,
            idioma_audio=self.idioma_audio,
            generos=self.get_lista_generos()
        )
