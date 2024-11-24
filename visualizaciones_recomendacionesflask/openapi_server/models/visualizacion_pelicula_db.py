from openapi_server import db

class VisualizacionPeliculaDB(db.Document):
    meta = {'collection': 'visualizaciones_pelicula'}  # Nombre de la colección en MongoDB

    id_perfil = db.IntField(required=True)
    pelicula_id = db.ObjectIdField()  

    def to_api_model(self):
        from openapi_server.models.visualizacion_pelicula import VisualizacionPelicula
        return VisualizacionPelicula(
            id_perfil=str(self.id_perfil),
            pelicula_id=str(self.pelicula_id),
        )