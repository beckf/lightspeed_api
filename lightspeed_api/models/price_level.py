
from . import BaseObject

class PriceLevel(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }