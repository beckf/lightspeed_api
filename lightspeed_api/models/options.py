
from . import BaseObject


class Option(BaseObject):
    _object_attributes = {
        "name": {"type": str, "ls_field": "name"},
        "value": {"type": str, "ls_field": "value"},
    }


class AccountOption(BaseObject):
    _object_attributes = {
        "id": {"type": 'Option', "multifield": True, "ls_field": "Option"},
    }