from openapi_server import db

class DispositivoDB(db.Model):

    __tablename__ = 'dispositivo'

    dispositivo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_dispositivo = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, tipo_dispositivo):  # noqa: E501
        self.tipo_dispositivo = tipo_dispositivo
