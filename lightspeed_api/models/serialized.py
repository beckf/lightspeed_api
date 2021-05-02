
from . import BaseObject

class SerializedItem(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }