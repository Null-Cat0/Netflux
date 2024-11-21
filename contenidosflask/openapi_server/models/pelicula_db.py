from openapi_server import db

from openapi_server.models.actor_db import ActorDB
from openapi_server.models.genero_db import GeneroDB

class PeliculaDB(db.Document):
    meta = {'collection': 'peliculas'}  # Nombre de la colección en MongoDB

    titulo = db.StringField(required=True)
    genero = db.ListField(db.ReferenceField(GeneroDB))
    sinopsis = db.StringField(required=True)
    anio_estreno = db.IntField(required=True)
    duracion = db.IntField(required=True)
    actores = db.ListField(db.ReferenceField(ActorDB)) 

    secuela = db.ReferenceField('self', required=False)
    precuela = db.ReferenceField('self', required=False)

    def to_api_model(self):
        from openapi_server.models.pelicula import Pelicula
        return Pelicula(
            id=str(self.id),  
            titulo=self.titulo,
            genero=[g.to_api_model() for g in self.genero],
            sinopsis=self.sinopsis,
            anio_estreno=self.anio_estreno,
            duracion=self.duracion,
            actores=[actor.to_api_model() for actor in self.actores] if self.actores else [],

            # Se retorna el título de la secuela y la precuela
            secuela=self.secuela.titulo if self.secuela else None,
            precuela=self.precuela.titulo if self.precuela else None
        )
