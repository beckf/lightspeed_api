
from . import BaseObject

class CreditCardCharge(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }