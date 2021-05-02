
from . import BaseObject


class Register(BaseObject):
    def __init__(self, obj=None, api=None):
        if obj:
            self.id = obj['registerID']
            self.name = obj['name']
    
    @property
    def active_sale(self):
        return self.api.sales.get_active_sale_at_register(self.id)
    
    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


class RegisterCount(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }


class RegisterCountAmount(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }


class RegisterWithdraw(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }