from openapi_server import util
from openapi_server import db

class DispositivoDB(db.Model):
    """
      NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
    	Do not edit the class manually.
    """

    __tablename__ = 'dispositivo'

    dispositivo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)

    def __init__(self, nombre=None):  # noqa: E501
        """DispositivoDB - a model defined 

        :param nombre: The nombre of this Dispositivo.  # noqa: E501
        :type nombre: str
        """
        self.openapi_types = {
            'dispositivo_id': int,
            'nombre': str,
        }

        self.attribute_map = {
            'dispositivo_id': 'dispositivo_id',
            'nombre': 'nombre',
        }

        self.nombre = nombre
    
    def serialize(self):
        return {
            'dispositivo_id': self.dispositivo_id,
            'nombre': self.nombre,
        }

    @classmethod
    def from_dict(cls, dikt) -> 'DispositivoDB':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DispositivoDB of this DispositivoDB.  # noqa: E501
        :rtype: DispositivoDB 
        """
        return util.deserialize_model(dikt, cls)