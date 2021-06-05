
from datetime import datetime

from . import BaseObject


class EmployeeRight(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "employeeRightID"},
        "name": {"type": str, "ls_field": "name"},
    }


class EmployeeRole(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "employeeRoleID"},
        "name": {"type": str, "ls_field": "name"},
        "emails": {"type": 'EmployeeRight', "multifield": True, "ls_field": "EmployeeRights"},
    }


class Employee(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "employeeID"},
        "first_name": {"type": str, "ls_field": "firstName"},
        "last_name": {"type": str, "ls_field": "lastName"},
        "is_locked_out": {"type": bool, "ls_field": "lockOut"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "customer": {"type": 'Customer', "ls_field": "Contact", "ls_field_id": "contactID", "relationships": ["Contact"]},   # TODO: might actually be a "Contact" object from a customer
        "currently_clocked_in_hours": {"type": 'EmployeeHours', "ls_field": "clockInEmployeeHoursID"},
        "role": {"type": 'EmployeeRole', "ls_field": "Contact", "ls_field_id": "contactID", "relationships": ["EmployeeRole", "EmployeeRole.EmployeeRights"]},
        "rights": {"type": 'EmployeeRight', "multifield": True, "ls_field": "EmployeeRights", "relationships": ["EmployeeRights"]},
        "limited_to_shop": {"type": 'Shop', "ls_field_id": "limitToShopID"},
        "last_shop": {"type": 'Shop', "ls_field_id": "lastShopID"},
        "last_sale": {"type": 'Sale', "ls_field_id": "lastSaleID"},
        "last_register": {"type": 'Register', "ls_field_id": "lastRegisterID"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
    }
    _update_url = 'Employee/%s.json'
    _create_url = 'Employee.json'
    _delete_url = 'Employee/%s.json'


class EmployeeHours(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "employeeHoursID"},
        "start": {"type": datetime, "ls_field": "checkIn"},
        "end": {"type": datetime, "ls_field": "checkOut"},
        "employee": {"type": 'Employee', "ls_field_id": "employeeID"},
        "shop": {"type": 'Shop', "ls_field_id": "shopID"},
    }
    _update_url = 'EmployeeHours/%s.json'
    _create_url = 'EmployeeHours.json'
    _delete_url = 'EmployeeHours/%s.json'