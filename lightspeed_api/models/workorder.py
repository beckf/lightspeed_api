
from datetime import datetime
from . import BaseObject

class Workorder(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "workorderID"},
        "received_time": {"type": datetime, "ls_field": "timeIn"},
        "estimated_out_time": {"type": datetime, "ls_field": "etaOut"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "note": {"type": str, "ls_field": "note"},
        "is_warrantied": {"type": bool, "ls_field": "warranty"},
        "is_taxed": {"type": bool, "ls_field": "tax"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "hook_in": {"type": str, "ls_field": "hookIn"},
        "hook_out": {"type": str, "ls_field": "hookOut"},
        "is_saving_parts": {"type": bool, "ls_field": "saveParts"},
        "is_same_employee_for_all_lines": {"type": bool, "ls_field": "assignEmployeeToAll"},
        "customer": {"type": 'Customer', "ls_field": "Customer", "ls_field_id": "customerID", "relationships": ["Customer"]},
        "discount": {"type": 'Discount', "ls_field": "Discount", "ls_field_id": "discountID", "relationships": ["Discount"]},
        "employee": {"type": 'Employee', "ls_field": "Employee", "ls_field_id": "employeeID", "relationships": ["Employee"]},
        "serialized_object": {"type": 'Serialized', "ls_field": "Serialized", "ls_field_id": "serializedID", "relationships": ["Serialized"]},
        "shop": {"type": 'Shop', "ls_field_id": "shopID"},
        "sale": {"type": 'Sale', "ls_field_id": "saleID"},
        "sale_line": {"type": 'SaleLine', "ls_field_id": "saleLineID"},
        "status": {"type": 'WorkorderStatus', "ls_field": "WorkorderStatus", "ls_field_id": "workorderStatusID", "relationships": ["WorkorderStatus"]},
        "items": {"type": 'WorkorderItem', "multifield": True, "ls_field": "WorkorderItems.WorkorderItem", "relationships": ["WorkorderItems"]},
        "lines": {"type": 'WorkorderLine', "multifield": True, "ls_field": "WorkorderLines.WorkorderLine", "relationships": ["WorkorderLines"]},
    }
    _get_function = "WorkordersAPI.get_workorder"


class WorkorderItem(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "workorderItemID"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "quantity": {"type": int, "ls_field": "unitQuantity"},
        "price": {"type": float, "ls_field": "unitPrice"},
        "is_approved": {"type": bool, "ls_field": "approved"},
        "is_warrantied": {"type": bool, "ls_field": "warranty"},
        "is_taxed": {"type": bool, "ls_field": "tax"},
        "is_special_order": {"type": bool, "ls_field": "isSpecialOrder"},
        "note": {"type": str, "ls_field": "note"},
        "workorder": {"type": 'Workorder', "ls_field_id": "workorderID"},
        "employee": {"type": 'Employee', "ls_field_id": "employeeID"},
        "sale_line": {"type": 'SaleLine', "ls_field_id": "saleLineID"},
        "sale": {"type": 'Sale', "ls_field_id": "saleID"},
        "item": {"type": 'Item', "ls_field_id": "itemID"},
        "discount": {"type": 'Discount', "ls_field": "Discount", "ls_field_id": "discountID", "relationships": ["Discount"]},
    }
    _get_function = "WorkordersAPI.get_workorder_item"


class WorkorderLine(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "workorderLineID"},
        "note": {"type": str, "ls_field": "note"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "hours": {"type": int, "ls_field": "hours"},
        "minutes": {"type": int, "ls_field": "minutes"},
        "price_override": {"type": float, "ls_field": "unitPriceOverride"},
        "quantity": {"type": int, "ls_field": "unitQuantity"},
        "cost": {"type": float, "ls_field": "unitCost"},
        "is_done": {"type": bool, "ls_field": "done"},
        "is_approved": {"type": bool, "ls_field": "approved"},
        "is_warrantied": {"type": bool, "ls_field": "warranty"},
        "is_taxed": {"type": bool, "ls_field": "tax"},
        "workorder": {"type": 'Workorder', "ls_field_id": "workorderID"},
        "employee": {"type": 'Employee', "ls_field_id": "employeeID"},
        "sale_line": {"type": 'SaleLine', "ls_field_id": "saleLineID"},
        "sale": {"type": 'Sale', "ls_field_id": "saleID"},
        "item": {"type": 'Item', "ls_field_id": "itemID"},
        "discount": {"type": 'Discount', "ls_field": "Discount", "ls_field_id": "discountID", "relationships": ["Discount"]},
        "tax_class": {"type": 'TaxClass', "ls_field": "TaxClass", "ls_field_id": "taxClassID", "relationships": ["TaxClass"]},
    }
    _get_function = "WorkordersAPI.get_workorder_line"


class WorkorderStatus(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "workorderStatusID"},
        "name": {"type": str, "ls_field": "name"},
        "sort_order": {"type": int, "ls_field": "sortOrder"},
        "color": {"type": str, "ls_field": "htmlColor"},
        "system_value": {"type": str, "ls_field": "systemValue"},
    }
    _get_function = "WorkordersAPI.get_workorder_status"
