
from datetime import datetime
from . import BaseObject


class SerializedItem(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "serializedID"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "color": {"type": str, "ls_field": "colorName"},
        "size": {"type": str, "ls_field": "sizeName"},
        "serial_numer": {"type": str, "ls_field": "serial"},
        "description": {"type": str, "ls_field": "description"},
        "item": {"type": 'Item', "ls_field": "itemID"},
        "sale_line": {"type": 'SaleLine', "ls_field": "saleLineID"},
        "customer": {"type": 'Customer', "ls_field": "customerID"},
    }