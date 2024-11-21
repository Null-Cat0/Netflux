from openapi_server import db

class ListaPerfilDB(db.Model):

    __tablename__ = 'lista_perfil'

    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil.perfil_id'), nullable=False)
    contenido = db.Column(db.String(255), nullable=False)
    es_serie = db.Column(db.Boolean, nullable=False, default=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('perfil_id', 'contenido'),
    )

    def __init__(self, perfil_id, contenido, es_serie=None):  # noqa: E501
        self.perfil_id = perfil_id
        self.contenido = contenido
        self.es_serie = es_serie
        
