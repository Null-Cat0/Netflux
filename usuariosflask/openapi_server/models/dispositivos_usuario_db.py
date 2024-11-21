from openapi_server import db

class DispositivosUsuarioDB(db.Model):

    __tablename__ = 'dispositivos_usuario'

    dispositivo_id = db.Column(db.Integer, db.ForeignKey('dispositivo.dispositivo_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.user_id'), nullable=False)
    nombre_dispositivo = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('dispositivo_id', 'user_id', 'nombre_dispositivo'),
    )

    def __init__(self, dispositivo_id, user_id, nombre_dispositivo):  # noqa: E501
        self.dispositivo_id = dispositivo_id
        self.user_id = user_id 
        self.nombre_dispositivo = nombre_dispositivo
