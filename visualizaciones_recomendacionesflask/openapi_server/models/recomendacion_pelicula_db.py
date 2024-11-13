from openapi_server import db

from openapi_server.models.pelicula_db import PeliculaDB

class RecomendacionPeliculaDB(db.Document):
    meta = {'collection': 'recomendaciones_pelicula'}  # Nombre de la colección en MongoDB

    id_perfil = db.IntField(required=True)

    peliculas_recomendadas = db.ListField(db.ReferenceField(PeliculaDB))

    def to_api_model(self):
        from openapi_server.models.recomendacion_pelicula import RecomendacionPelicula
        return RecomendacionPelicula(
            id_recomendacion_pelicula=str(self.id_recomendacion_pelicula),
            id_perfil=self.id_perfil,
            peliculas_recomendadas=[pelicula.to_api_model() for pelicula in self.peliculas_recomendadas] if self.peliculas_recomendadas else []
        )