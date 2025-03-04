from openapi_server import db
from datetime import datetime

class HistorialPerfilDB(db.Model):

    __tablename__ = 'historial_perfil'

    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil.perfil_id'), nullable=False)
    contenido = db.Column(db.String(255), nullable=False)
    es_capitulo = db.Column(db.Boolean, nullable=False, default=False)
    fecha_visualizacion = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    __table_args__ = (
        db.PrimaryKeyConstraint('perfil_id', 'contenido'),
    )

    def __init__(self, perfil_id, contenido, es_capitulo=None):  # noqa: E501
        self.perfil_id = perfil_id
        self.contenido = contenido
        self.es_capitulo = es_capitulo
        self.fecha_visualizacion = datetime.now()