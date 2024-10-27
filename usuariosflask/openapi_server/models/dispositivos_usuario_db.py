from openapi_server import util
from openapi_server import db

class DispositivosUsuarioDB(db.Model):

    __tablename__ = 'dispositivos_usuario'

    dispositivo_id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)

    def __init__(self, dispositivo_id, user_id):  # noqa: E501
        self.dispositivo_id = dispositivo_id
        self.user_id = user_id 