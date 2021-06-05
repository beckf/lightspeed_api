
from . import BaseObject

class PaymentType(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "paymentTypeID"},
        "name": {"type": str, "ls_field": "name"},
        "is_require_customer": {"type": bool, "ls_field": "requireCustomer"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "is_internal_type": {"type": bool, "ls_field": "internalReserved"},
        "id": {"type": str, "ls_field": "type"},        # TODO: enum
        "refunded_payment_type": {"type": 'PaymentType', "ls_field": "refundAsPaymentTypeID"},
    }