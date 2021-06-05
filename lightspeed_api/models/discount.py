
from datetime import datetime

from . import BaseObject


class Discount(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "discountID"},
        "name": {"type": str, "ls_field": "name"},
        "amount": {"type": float, "ls_field": "discountAmount"},
        "percentage": {"type": float, "ls_field": "discountPercent"},
        "is_customer_required": {"type": bool, "ls_field": "requireCustomer"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
    }
    _update_url = 'Discount/%s.json'
    _create_url = 'Discount.json'
    _delete_url = 'Discount/%s.json'