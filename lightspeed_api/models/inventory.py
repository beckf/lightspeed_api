
from datetime import datetime

from . import BaseObject

class InventoryCount(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "inventoryCountID"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "name": {"type": str, "ls_field": "name"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "shop": {"type": 'Shop', "ls_field_id": "shopID"},
    }


class InventoryCountItem(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "inventoryCountItemID"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "quantity": {"type": int, "ls_field": "qty"},
        "inventory": {"type": 'InventoryCount', "ls_field_id": "inventoryCountID"},
        "employee": {"type": 'Employee', "ls_field_id": "employeeID"},
        "item": {"type": 'Item', "ls_field_id": "itemID"},
    }


class InventoryCountCalculation(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "inventoryCountCalcID"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "expected_count": {"type": int, "ls_field": "calcQoh"},
        "actual_count": {"type": int, "ls_field": "countedQoh"},
        "inventory": {"type": 'InventoryCount', "ls_field_id": "inventoryCountID"},
        "item": {"type": 'Item', "ls_field_id": "shopID"},
    }


class InventoryCountReconciliation(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "inventoryCountReconcileID"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "cost_change": {"type": float, "ls_field": "costChange"},
        "count_change": {"type": int, "ls_field": "qohChange"},
        "inventory": {"type": 'InventoryCount', "ls_field_id": "inventoryCountID"},
        "item": {"type": 'Item', "ls_field_id": "shopID"},
    }


class InventoryTransfer(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "transferID"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "note": {"type": str, "ls_field": "note"},
        "status": {"type": str, "ls_field": "status"},
        "sent_time": {"type": datetime, "ls_field": "sentOn"},
        "needed_by_time": {"type": datetime, "ls_field": "needBy"},
        "created_employee": {"type": 'Employee', "ls_field_id": "sentByEmployeeID", "relationships": ["CreatedByEmployee", "CreatedByEmployee.Contact"]},
        "sending_employee": {"type": 'Employee', "ls_field_id": "sentByEmployeeID", "relationships": ["SentByEmployee", "SentByEmployee.Contact"]},
        "sending_shop": {"type": 'Shop', "ls_field_id": "sendingShopID", "relationships": ["SendingShop", "SendingShop.Contact"]},
        "receiving_shop": {"type": 'Shop', "ls_field_id": "receivingShopID", "relationships": ["ReceivingShop", "ReceivingShop.Contact"]},
    }

class InventoryTransferItem(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "transferItemID"},
        "count_sending": {"type": int, "ls_field": "toSend"},
        "count_receiving": {"type": int, "ls_field": "toReceive"},
        "currently_sent": {"type": int, "ls_field": "sent"},
        "currently_received": {"type": int, "ls_field": "received"},
        "value_sent": {"type": float, "ls_field": "sentValue"},
        "value_received": {"type": float, "ls_field": "receivedValue"},
        "comment": {"type": str, "ls_field": "comment"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "transfer": {"type": 'InventoryTransfer', "ls_field_id": "transferID"},
        "item": {"type": 'Item', "ls_field_id": "itemID"},
    }