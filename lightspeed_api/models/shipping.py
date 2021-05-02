
from . import BaseObject

class ShipTo(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }