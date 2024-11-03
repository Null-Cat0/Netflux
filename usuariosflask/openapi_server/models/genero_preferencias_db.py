from openapi_server import util
from openapi_server import db

class GeneroPreferenciasDB(db.Model):

    __tablename__ = 'genero_preferencias'

    perfil_id = db.Column(db.Integer, db.ForeignKey('preferencias_contenido.perfil_id'), nullable=False)
    genero_id = db.Column(db.Integer, db.ForeignKey('genero.genero_id'), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('perfil_id', 'genero_id'),
    )

    def __init__(self, perfil_id, genero_id):  # noqa: E501
        self.perfil_id = dispositivo_id
        self.genero_id = genero_id