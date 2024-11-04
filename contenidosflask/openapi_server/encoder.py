from flask.json import JSONEncoder
from openapi_server.models.base_model import Model

class CustomJSONEncoder(JSONEncoder):
    include_nulls = False

    def default(self, o):
        if isinstance(o, Model):
            dikt = {}
            for attr in o.openapi_types:
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        return super().default(o)  # Usa el método default del JSONEncoder de Flask