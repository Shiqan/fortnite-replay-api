from flask import json
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemySerializer(json.JSONEncoder):
    ''' Custom json serializer for SqlAlchemy models
    
    Add a __json__ method to your model which returns a list of property names.
    ''' 
    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            data = {}
            fields = o.__json__() if hasattr(o, '__json__') else []
            for field in fields:
                value = o.__getattribute__(field)
                try:
                    json.dumps(value)
                    data[field] = value
                except TypeError:
                    data[field] = None
            return data
        return json.JSONEncoder.default(self, o)
