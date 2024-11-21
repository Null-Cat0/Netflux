from openapi_server import db

from openapi_server.models.actor_db import ActorDB
from openapi_server.models.genero_db import GeneroDB

from bson import ObjectId

class CapituloEmbeddedDB(db.EmbeddedDocument):
    capitulo_id = db.ObjectIdField(default=ObjectId)
    numero = db.IntField(required=True)
    titulo = db.StringField(required=True)
    duracion = db.IntField(required=True)  # Duración en minutos
    sinopsis = db.StringField()

    def to_api_model(self):
        from openapi_server.models.serie import CapituloEmbedded
        return CapituloEmbedded(
            capitulo_id=str(self.capitulo_id),
            numero=self.numero,
            titulo=self.titulo,
            duracion=self.duracion,
            sinopsis=self.sinopsis
        )

class TemporadaEmbeddedDB(db.EmbeddedDocument):
    temporada_id = db.ObjectIdField(default=ObjectId)
    numero = db.IntField(required=True)
    anio_lanzamiento = db.IntField(required=True)
    capitulos = db.ListField(db.EmbeddedDocumentField(CapituloEmbeddedDB))

    def to_api_model(self):
        from openapi_server.models.serie import TemporadaEmbedded
        return TemporadaEmbedded(
            temporada_id=str(self.temporada_id),
            numero=self.numero,
            anio_lanzamiento=self.anio_lanzamiento,
            capitulos=[capitulo.to_api_model() for capitulo in self.capitulos]
        )

class SerieDB(db.Document):
    meta = {'collection': 'series'}

    titulo = db.StringField(required=True)
    genero = db.ListField(db.ReferenceField(GeneroDB))
    sinopsis = db.StringField(required=True)
    anio_estreno = db.IntField(required=True)
    temporadas = db.ListField(db.EmbeddedDocumentField(TemporadaEmbeddedDB))  # Temporadas con capítulos anidados
    actores = db.ListField(db.ReferenceField(ActorDB))

    def to_api_model(self):
        from openapi_server.models.serie import Serie
        return Serie(
            id=str(self.id),
            titulo=self.titulo,
            genero=[genero.to_api_model() for genero in self.genero] if self.genero else [],
            sinopsis=self.sinopsis,
            anio_estreno=self.anio_estreno,
            temporadas=[temporada.to_api_model() for temporada in self.temporadas] if self.temporadas else [],
            actores=[actor.to_api_model() for actor in self.actores] if self.actores else []
        )
