from openapi_server import db

class CapituloEmbedded(db.EmbeddedDocument):
    numero = db.IntField(required=True)
    titulo = db.StringField(required=True)
    duracion = db.IntField(required=True)  # Duración en minutos
    sinopsis = db.StringField()

class TemporadaEmbedded(db.EmbeddedDocument):
    numero = db.IntField(required=True)
    anio_lanzamiento = db.IntField(required=True)
    capitulos = db.ListField(db.EmbeddedDocumentField(CapituloEmbedded))

class Serie(db.Document):
    meta = {'collection': 'series'}

    id = db.IntField(primary_key=True)
    titulo = db.StringField(required=True)
    genero = db.StringField(required=True)
    sinopsis = db.StringField(required=True)
    anio_estreno = db.IntField(required=True)
    temporadas = db.ListField(db.EmbeddedDocumentField(TemporadaEmbedded))  # Temporadas con capítulos anidados
    actores = db.ListField(db.ReferenceField('Actor'))

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "sinopsis": self.sinopsis,
            "anio_estreno": self.anio_estreno,
            "temporadas": [temporada.to_mongo().to_dict() for temporada in self.temporadas],
            "actores": [actor.to_dict() for actor in self.actores] if self.actores else []
        }
