from openapi_server import db

class ActorDB(db.Document):
    meta = {'collection': 'actores'}

    # No se especifica el id porque se genera automáticamente
    nombre = db.StringField(required=True)
    fecha_nacimiento = db.DateField(required=False)
    nacionalidad = db.StringField(required=False)
    biografia = db.StringField(required=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_nacimiento": self.fecha_nacimiento,
            "nacionalidad": self.nacionalidad,
            "biografia": self.biografia
        }

    def to_api_model(self):
        from openapi_server.models.actor import Actor
        return Actor(
            id=str(self.id),
            nombre=self.nombre,
            fecha_nacimiento=self.fecha_nacimiento,
            nacionalidad=self.nacionalidad,
            biografia=self.biografia
        )
