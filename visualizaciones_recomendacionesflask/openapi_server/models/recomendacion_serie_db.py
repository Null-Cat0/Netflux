from openapi_server import db

class RecomendacionSerieDB(db.Document):
    meta = {'collection': 'recomendaciones_serie'}  # Nombre de la colección en MongoDB

    id_perfil = db.IntField(required=True)
    series_recomendadas = db.ListField()

    def to_api_model(self):
        from openapi_server.models.recomendacion_serie import RecomendacionSerie
        return RecomendacionSerie(
            id_perfil=self.id_perfil,
            series_recomendadas=self.series_recomendadas or []
        )