from openapi_server import db

class VisualizacionCapituloDB(db.Document):
    meta = {'collection': 'visualizaciones_capitulo'}  # Nombre de la colección en MongoDB

    id_perfil = db.IntField(required=True)
    serie_id = db.ObjectIdField()
    temporada_id = db.ObjectIdField()
    capitulo_id = db.ObjectIdField()
    fecha_visualizacion = db.DateTimeField()

    def to_api_model(self):
        from openapi_server.models.visualizacion_pelicula import VisualizacionPelicula
        return VisualizacionPelicula(
            id_perfil=self.id_perfil,
            capitulo_id=self.id_pelicula,
            fecha_visualizacion=self.fecha_visualizacion
        )