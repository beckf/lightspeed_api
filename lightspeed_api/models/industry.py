
from . import BaseObject

class Industry(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "industryID"},
        "name": {"type": str, "ls_field": "name"},
        "is_enabled": {"type": bool, "ls_field": "enabled"},
    }