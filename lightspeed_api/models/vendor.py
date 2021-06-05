
from datetime import datetime
from . import BaseObject

class VendorRepresentative(BaseObject):
    _object_attributes = {
        "first_name": {"type": str, "ls_field": "firstName"},
        "last_name": {"type": str, "ls_field": "lastName"},
        "name": {"combine": ["first_name", "last_name"]},
    }

class Vendor(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "vendorID"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "name": {"type": str, "ls_field": "name"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "account_number": {"type": str, "ls_field": "accountNumber"},
        "price_level": {"type": str, "ls_field": "priceLevel"},
        "is_update_price": {"type": bool, "ls_field": "updatePrice"},
        "is_update_cost": {"type": bool, "ls_field": "updateCost"},
        "is_update_description": {"type": bool, "ls_field": "updateDescription"},
        "is_sell_through_data_enabled": {"type": bool, "ls_field": "shareSellThrough"},
        "contact": {"type": 'Contact', "optional": True, "ls_field": "Contact", "relationships": ["Contact"]},
        "representatives": {"type": 'VendorRepresentative', "multifield": True, "ls_field": "Reps.VendorRep"},
    }
    _get_function = "VendorsAPI.get_vendor"
    _update_url = 'Vendor/%s.json'
    _create_url = 'Vendor.json'
    
    def delete(self):
        self.api.request('DELETE', f'Vendor/{self.id}.json')

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)