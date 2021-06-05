
from datetime import datetime

from . import BaseObject


class CreditAccount(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "creditAccountID"},
        "name": {"type": str, "ls_field": "name"},
        "code": {"type": str, "ls_field": "code"},
        "description": {"type": str, "ls_field": "description"},
        "is_giftcard": {"type": bool, "ls_field": "giftCard"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "customer": {"type": 'Customer', "ls_field": "Contact", "ls_field_id": "customerID", "relationships": ["Contact"]},   # TODO: might actually be a "Contact" object from a customer
        "withdrawals": {"type": 'SalePayment', "multifield": True, "ls_field": "WithdrawalPayments.Payment", "relationships": ["WithdrawalPayments"]},
        "last_modified_time": {"type": int, "ls_field": "timeStamp"},
        "balance": {"type": float, "ls_field": "balance"},
    }
    _get_function = "CreditAccountsAPI.get_customer"
    _update_url = 'CreditAccount/%s.json'
    _create_url = 'CreditAccount.json'
    _delete_url = 'CreditAccount/%s.json'