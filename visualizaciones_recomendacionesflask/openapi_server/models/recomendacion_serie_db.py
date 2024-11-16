from openapi_server import db

from openapi_server.models.serie_db import SerieDB

class RecomendacionSerieDB(db.Document):
    meta = {'collection': 'recomendaciones_serie'}  # Nombre de la colección en MongoDB

    id_perfil = db.IntField(required=True)

    serie_recomendadas = db.ListField(db.ReferenceField(SerieDB))

    def to_api_model(self):
        from openapi_server.models.recomendacion_serie import RecomendacionSerie
        return RecomendacionSerie(
            id_recomendacion_serie=str(self.id_recomendacion_serie),
            id_perfil=self.id_perfil,
            series_recomendadas=[serie.to_api_model() for serie in self.series_recomendadas] if self.series_recomendadas else []
        )