
from datetime import datetime
from . import BaseObject


class Register(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "registerID"},
        "name": {"type": str, "ls_field": "name"},
        "is_open": {"type": bool, "ls_field": "open"},
        "opened_time": {"type": datetime, "ls_field": "openTime"},
        "opened_by_employee": {"type": 'Employee', "ls_field": "openEmployeeID"},
        "shop": {"type": 'Shop', "ls_field": "shopID"},
    }
    _get_function = "RegistersAPI.get_register"
    _update_url = 'Register/%s.json'
    _create_url = 'Register.json'
    
    @property
    def active_sale(self):
        return self.api.sales.get_active_sale_at_register(self.id)
    
    def close(self):
        pass
    
    def open(self):
        pass
    
    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


class RegisterCount(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "registerCountID"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "opened_time": {"type": datetime, "ls_field": "openTime"},
        "notes": {"type": str, "ls_field": "notes"},
        "register": {"type": 'Register', "ls_field": "registerID"},
        "opened_by_employee": {"type": 'Employee', "ls_field": "openEmployeeID"},
        "closed_by_employee": {"type": 'Employee', "ls_field": "closeEmployeeID"},
        "amounts": {"type": 'RegisterCountAmount', "multifield": True, "ls_field": "RegisterCountAmounts.RegisterCountAmount", "relationships": ["RegisterCountAmounts", "RegisterCountAmounts.PaymentType"]},
    }


class RegisterCountAmount(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "registerCountAmountID"},
        "calculated_amount": {"type": float, "ls_field": "calculated"},
        "actual_amount": {"type": float, "ls_field": "actual"},
        "register": {"type": 'Register', "ls_field": "registerCountID"},
        "payment_type": {"type": 'PaymentType', "ls_field": "PaymentType", "ls_field_id": "paymentTypeID", "relationships": ["PaymentType"]},
    }


class RegisterWithdraw(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "registerWithdrawID"},
        "amount": {"type": float, "ls_field": "amount"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "notes": {"type": str, "ls_field": "notes"},
        "register": {"type": 'Register', "ls_field": "registerID"},
        "employee": {"type": 'Employee', "ls_field": "employeeID"},
        "payment_type": {"type": 'PaymentType', "ls_field": "PaymentType", "ls_field_id": "paymentTypeID", "relationships": ["PaymentType"]},
    }


class ReceiptSetup(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "receiptSetupID"},
        "general_message": {"type": str, "ls_field": "generalMsg"},
        "workorder_agreement": {"type": str, "ls_field": "workorderAgree"},
        "credit_card_agreement": {"type": str, "ls_field": "creditcardAgree"},
        "logo_url": {"type": str, "ls_field": "logo"},
        "logo_height": {"type": int, "ls_field": "logoHeight"},
        "logo_width": {"type": int, "ls_field": "logoWidth"},
        "header": {"type": str, "ls_field": "header"},
    }