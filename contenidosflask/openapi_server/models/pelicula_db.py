from openapi_server import db

class PeliculaDB(db.Document):
    meta = {'collection': 'peliculas'}  # Nombre de la colección en MongoDB

    titulo = db.StringField(required=True)
    genero = db.StringField(required=True)
    sinopsis = db.StringField(required=True)
    anio_estreno = db.IntField(required=True)
    duracion = db.IntField(required=True)
    actores = db.ListField(db.ObjectIdField())  # Lista de IDs de actores como ObjectId

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "sinopsis": self.sinopsis,
            "anio_estreno": self.anio_estreno,
            "duracion": self.duracion,
            "actores": self.actores
        }

    def to_api_model(self):
        from openapi_server.models.pelicula import Pelicula
        from openapi_server.models.actor_db import ActorDB
        return Pelicula(
            id=str(self.id),  
            titulo=self.titulo,
            genero=self.genero,
            sinopsis=self.sinopsis,
            anio_estreno=self.anio_estreno,
            duracion=self.duracion,
            actores=[actor.to_api_model() for actor in ActorDB.objects(id__in=self.actores)]
        )
