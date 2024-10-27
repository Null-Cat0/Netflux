from openapi_server import util
from openapi_server import db

class DispositivoDB(db.Model):

    __tablename__ = 'dispositivo'

    dispositivo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)

    def __init__(self, nombre=None):  # noqa: E501
        self.nombre = nombre