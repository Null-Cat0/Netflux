from openapi_server import util
from openapi_server import db

class ListaPerfilDB(db.Model):

    __tablename__ = 'lista_perfil'

    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil.perfil_id'), nullable=False)
    contenido = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('perfil_id', 'contenido'),
    )

    def __init__(self, perfil_id, contenido):  # noqa: E501
        self.perfil_id = perfil_id
        self.contenido = contenido
        