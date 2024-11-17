from openapi_server import util
from openapi_server import db

class GeneroPreferenciasDB(db.Model):

    __tablename__ = 'genero_preferencias'

    preferencias_id = db.Column(db.Integer, db.ForeignKey('preferencias_contenido.preferencias_id'), nullable=False)
    genero_id = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('preferencias_id', 'genero_id'),
    )

    def __init__(self, preferencias_id, genero_id):  # noqa: E501
        self.preferencias_id = preferencias_id
        self.genero_id = genero_id