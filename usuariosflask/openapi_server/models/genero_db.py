from openapi_server import util
from openapi_server import db

class GeneroDB(db.Model):

    __tablename__ = 'genero'

    genero_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, nombre):  # noqa: E501
        self.nombre = nombre