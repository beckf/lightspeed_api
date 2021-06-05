
from datetime import datetime
from . import BaseObject


class ShipTo(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "shipToID"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "is_shipped": {"type": bool, "ls_field": "shipped"},
        "notes": {"type": str, "ls_field": "shipNote"},
        "first_name": {"type": str, "ls_field": "firstName"},
        "last_name": {"type": str, "ls_field": "lastName"},
        "customer": {"type": 'Customer', "ls_field_id": "customerID"},
        "sale": {"type": 'Sale', "ls_field_id": "saleID"},
        "shipping_address": {"type": 'Contact', "ls_field": "Contact", "relationships": ["Contact"]},       # TODO: contact mapping be different
    }