
from datetime import datetime
from . import BaseObject


class Order(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "orderID"},
        "ordered_time": {"type": datetime, "ls_field": "orderedDate"},
        "received_time": {"type": datetime, "ls_field": "receivedDate"},
        "arrival_time": {"type": datetime, "ls_field": "arrivalDate"},
        "reference_number": {"type": str, "ls_field": "refNum"},
        "shipping_instructions": {"type": str, "ls_field": "shipInstructions"},
        "stock_instructions": {"type": str, "ls_field": "stockInstructions"},
        "shipping_costs": {"type": float, "ls_field": "shipCost"},
        "other_costs": {"type": float, "ls_field": "otherCost"},
        "is_complete": {"type": bool, "ls_field": "complete"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "discount_percent": {"type": float, "ls_field": "discount"},
        "total_discount": {"type": float, "ls_field": "totalDiscount"},
        "total_quantity": {"type": int, "ls_field": "totalQuantity"},
        "vendor": {"type": 'Vendor', "ls_field": "Vendor", "ls_field_id": "vendorID", "relationships": ["Vendor"]},
        "note": {"type": 'Note', "ls_field": "Note", "ls_field_id": "noteID", "relationships": ["Note"]},
        "shop": {"type": 'Shop', "ls_field": "Shop", "ls_field_id": "shopID", "relationships": ["Shop"]},
        "custom_fields": {"type": 'OrderCustomFieldValue', "multifield": True, "ls_field": "CustomFieldValues.CustomFieldValue", "relationships": ["CustomFieldValues", "CustomFieldValues.value"]},
        "lines": {"type": 'OrderLine', "multifield": True, "ls_field": "OrderLines.OrderLine", "relationships": ["OrderLines"]},
    }


class OrderLine(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "orderLineID"},
        "quantity": {"type": int, "ls_field": "quantity"},
        "price": {"type": float, "ls_field": "price"},
        "original_price": {"type": float, "ls_field": "originalPrice"},
        "count_checked_in": {"type": int, "ls_field": "checkedIn"},
        "count_received": {"type": int, "ls_field": "numReceived"},
        "total": {"type": float, "ls_field": "total"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "order": {"type": 'Order', "ls_field_id": "orderID"},
        "item": {"type": 'Item', "ls_field_id": "itemID"},
    }


class OrderCustomField(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
        "name": {"type": str, "ls_field": "name"},
        "type": {"type": str, "ls_field": "type"},
        "units": {"type": str, "ls_field": "uom"},
        "decimal_precision": {"type": int, "ls_field": "decimalPrecision"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "default": {"type": str, "ls_field": "default"},    # TODO: may be a mixed type, so this may not work?
    }


class OrderCustomFieldValue(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldValueID"},
        "custom_field": {"type": 'OrderCustomField', "ls_field_id": "customFieldID"},
        "is_deleted": {"type": bool, "ls_field": "deleted"},
        "name": {"type": str, "ls_field": "name"},
        "type": {"type": str, "ls_field": "type"},      # TODO: do we want to convert this to a Python type?
        "value": {"type": str, "ls_field": "value"},    # TODO: do we want to convert this to its Python type?
    }


class OrderCustomFieldChoice(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldChoiceID"},
        "name": {"type": str, "ls_field": "name"},
        "value": {"type": str, "ls_field": "value"},
        "is_deletable": {"type": bool, "ls_field": "canBeDeleted"},
        "custom_field": {"type": 'OrderCustomField', "ls_field_id": "customFieldID"},
    }