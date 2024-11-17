from openapi_server import db

class RecomendacionPeliculaDB(db.Document):
    meta = {'collection': 'recomendaciones_pelicula'}  # Nombre de la colección en MongoDB

    id_perfil = db.IntField(required=True)
    peliculas_recomendadas = db.ListField()

    def to_api_model(self):
        from openapi_server.models.recomendacion_pelicula import RecomendacionPelicula
        return RecomendacionPelicula(
            id_perfil=self.id_perfil,
            peliculas_recomendadas=self.peliculas_recomendadas or []
        )