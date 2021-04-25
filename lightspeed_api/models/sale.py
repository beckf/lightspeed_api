
from datetime import datetime
from . import BaseObject


class Sale(BaseObject):
    def __init__(self, obj=None, api=None):
        if obj:
            self.id = obj['saleID']
            self.timestamp = obj['timeStamp']
            self.completed = obj['completed']
            self.total = obj['calcTotal']
            self.customer_id = obj['customerID']
            self.internal_note_id = "0" if "SaleNotes" not in obj or "InternalNote" not in obj["SaleNotes"] else obj["SaleNotes"]["InternalNote"]['noteID']
            self.internal_note = "" if self.internal_note_id == "0" else obj["SaleNotes"]["InternalNote"]["note"]
            self.printed_note_id = "0" if "SaleNotes" not in obj or "PrintedNote" not in obj["SaleNotes"] else obj["SaleNotes"]["PrintedNote"]['noteID']
            self.printed_note = "" if self.printed_note_id == "0" else obj["SaleNotes"]["PrintedNote"]['note']
            self._obj = obj
    
    @property
    def items(self):
        return self.api.sales.get_all_from_sale(self.id)
    
    def has_customer(self):
        return self.customer_id != "0"

    @property
    def customer(self):
        if self.customer_id == "0":
            return None
        return self.api.customers.get_customer(self.customer_id)
    
    def set_note(self, note):
        return self.api.sales.set_note(self.id, note)


class SaleLineItem(BaseObject):
    def __init__(self, obj=None, api=None):
        if obj:
            self.id = obj['saleLineID']
            self.sale_id = obj['saleID']
            self.item_id = obj['itemID']
            self.created_at = obj['createTime']
            self.total = obj['calcTotal']
            self.count = int(obj['unitQuantity'])
            self._obj = obj
    
    @property
    def tags(self):
        return self.api.items.get_tags_for_item(self.item_id)
    
    @property
    def item(self):
        return self.api.items.get_item(self.item_id)

    @property
    # TODO: figure out how to pass in the object (if it existed) instead of re-looking it up.
    def sale(self):
        return self.api.sales.get_sale(self.sale_id)
    
    def set_note(self, note):
        return self.api.sales.set_item_note(self.id, self.sale_id, note)


class Quote(BaseObject):
    search_terms = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }


class SalePayment(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }


class SaleVoid(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }


class SpecialOrder(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }