from openapi_server import db

class VisualizacionCapituloDB(db.Document):
    meta = {'collection': 'visualizaciones_capitulo'}  # Nombre de la colección en MongoDB

    id_perfil = db.IntField(required=True)
    serie_id = db.ObjectIdField()
    temporada_id = db.ObjectIdField()
    capitulo_id = db.ObjectIdField()
    fecha_visualizacion = db.DateTimeField()

    def to_api_model(self):
        from openapi_server.models.visualizacion_capitulo import VisualizacionCapitulo
        return VisualizacionCapitulo(
            id_perfil=str(self.id_perfil),
            serie_id=str(self.serie_id),
            temporada_id=str(self.temporada_id),
            capitulo_id=str(self.capitulo_id),
            fecha_visualizacion=self.fecha_visualizacion
        )