from openapi_server import db
from openapi_server.models.actor_db import ActorDB

class PeliculaDB(db.Document):
    meta = {'collection': 'peliculas'}  # Nombre de la colección en MongoDB

    titulo = db.StringField(required=True)
    genero = db.ListField(db.StringField(), required=True)
    sinopsis = db.StringField(required=True)
    anio_estreno = db.IntField(required=True)
    duracion = db.IntField(required=True)
    actores = db.ListField(db.ReferenceField(ActorDB)) 

    def to_api_model(self):
        from openapi_server.models.pelicula import Pelicula
        return Pelicula(
            id=str(self.id),  
            titulo=self.titulo,
            genero=self.genero,
            sinopsis=self.sinopsis,
            anio_estreno=self.anio_estreno,
            duracion=self.duracion,
            actores=[actor.to_api_model() for actor in self.actores]
        )
