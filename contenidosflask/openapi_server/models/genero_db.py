from openapi_server import db

class GeneroDB(db.Document):
    meta = {'collection': 'generos'}  # Nombre de la colección en MongoDB

    nombre = db.StringField(required=True, unique=True)

    def to_api_model(self):
        from openapi_server.models.genero import Genero
        return Genero(
            id=str(self.id),
            nombre=self.nombre
        )
