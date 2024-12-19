from openapi_server import db

from openapi_server.models.dispositivo_db import DispositivoDB

from openapi_server.models.perfil_db import PerfilDB # No sobra este import 
from openapi_server.models.dispositivos_usuario_db import DispositivosUsuarioDB

class UsuarioDB(db.Model):

    __tablename__ = 'usuario'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    correo_electronico = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    pais = db.Column(db.String(255))
    plan_suscripcion = db.Column(db.String(255))
    esAdmin = db.Column(db.Boolean, default=False)
    

    perfiles = db.relationship('PerfilDB', backref='usuario', cascade='all, delete')
    dispositivos = db.relationship('DispositivosUsuarioDB', backref='usuario', cascade='all, delete')

    def __init__(self, nombre, correo_electronico, password, pais, plan_suscripcion, esAdmin):  # noqa: E501
        self.nombre = nombre
        self.correo_electronico = correo_electronico
        self.password = password
        self.pais = pais
        self.plan_suscripcion = plan_suscripcion
        self.esAdmin = esAdmin
    
    def get_dispositivos(self):
        dispositivos_ids = [dispositivo.dispositivo_id for dispositivo in self.dispositivos]
        dispositivos = [tipo_dispositivo for (tipo_dispositivo,) in db.session.query(DispositivoDB.tipo_dispositivo).filter(DispositivoDB.dispositivo_id.in_(dispositivos_ids)).all()]
        return dispositivos
    
    def to_api_model(self):
        from openapi_server.models.usuario import Usuario
        return Usuario(
            user_id=self.user_id,
            nombre=self.nombre,
            correo_electronico=self.correo_electronico,
            password=self.password,
            pais=self.pais,
            plan_suscripcion=self.plan_suscripcion,
            dispositivos=self.get_dispositivos(),
            perfiles=[perfil.to_api_model() for perfil in self.perfiles],
            esAdmin=self.esAdmin
        )
