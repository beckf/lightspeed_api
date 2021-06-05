
from . import BaseObject

class Session(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "sessionID"},
        "session_cookie": {"type": str, "ls_field": "sessionCookie"},
        "employee": {"type": 'Employee', "ls_field_id": "employeeID"},
        "account_id": {"type": int, "ls_field_id": "systemCustomerID"},
        "employee_user_id": {"type": int, "ls_field_id": "systemUserID"},
        "api_client_id": {"type": int, "ls_field_id": "systemAPIClientID"},
        "api_key_id": {"type": int, "ls_field_id": "systemAPIKeyID"},
        "shop_count": {"type": int, "ls_field_id": "shopCount"},
    }