
from . import BaseObject

class Workorder(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }


class WorkorderItem(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }


class WorkorderLine(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }


class WorkorderStatus(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }