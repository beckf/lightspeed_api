
from . import BaseObject

class Industry(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }