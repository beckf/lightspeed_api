
from datetime import datetime, date
from enum import Enum

from . import BaseObject

from ..api import ClientAPI


class CustomerType(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customerTypeID"},
        "name": {"type": str, "ls_field": "name"},
        "tax_category": {"type": 'TaxCategory', "ls_field": "TaxCategory", "ls_field_id": "taxCategoryID", "relationships": ["TaxCategory"]},     # TODO: there are TaxCategory.TaxCategoryClasses and TaxCategory.TaxCategoryClasses.TaxClass relationships for this item too - should we load them all?
        "discount": {"type": 'Discount', "ls_field": "Discount", "ls_field_id": "discountID", "relationships": ["Discount"]}
    }
    _get_function = "CustomersAPI.get_customer_type"


class CustomerCustomField(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
        "name": {"type": str, "ls_field": "name"},
        "type": {"type": str, "ls_field": "type"},
        "units": {"type": str, "ls_field": "uom"},
        "decimal_precision": {"type": int, "ls_field": "decimalPrecision"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "default": {"type": str, "ls_field": "default"},    # TODO: may be a mixed type, so this may not work?
    }
    _get_function = "CustomersAPI.get_customer_custom_field"


class CustomerCustomFieldValue(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldValueID"},
        "custom_field": {"type": 'CustomerCustomField', "ls_field_id": "customFieldID"},
        #"is_deleted": {"type": bool, "ls_field": "deleted"},
        "name": {"type": str, "ls_field": "name"},
        "type": {"type": str, "ls_field": "type"},      # TODO: do we want to convert this to a Python type?
        "value": {"type": str, "ls_field": "value"},    # TODO: do we want to convert this to its Python type?
    }


class CustomerCustomFieldChoice(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldChoiceID"},
        "name": {"type": str, "ls_field": "name"},
        "value": {"type": str, "ls_field": "value"},
        "is_deletable": {"type": bool, "ls_field": "canBeDeleted"},
        "custom_field": {"type": 'CustomerCustomField', "ls_field_id": "customFieldID"},
    }


class CustomerEmailType(Enum):
    PRIMARY = "Primary"
    SECONDARY = "Secondary"

    def __str__(self):
        return self.value


class CustomerEmail(BaseObject):
    _object_attributes = {
        "address": {"type": str, "ls_field": "address"},
        "type": {"type": str, "ls_field": "useType", "convert_class": CustomerEmailType},
    }

    def __init__(self, address, address_type):
        # TODO: figure out how to do this more elegantly :/ decorator perhaps?
        if isinstance(address_type, ClientAPI):
            super().__init__(address, address_type)         # Actually meant to be an upper call
        else:
            self.address = address
            self.type = address_type


class CustomerPhoneNumberType(Enum):
    HOME = "Home"
    WORK = "Work"
    PAGER = "Pager"
    MOBILE = "Mobile"
    FAX = "Fax"

    def __str__(self):
        return self.value


class CustomerPhoneNumber(BaseObject):
    _object_attributes = {
        "number": {"type": str, "ls_field": "number"},
        "type": {"type": str, "ls_field": "useType", "convert_class": CustomerPhoneNumberType},
    }

    def __init__(self, number, number_type):
        # TODO: figure out how to do this more elegantly :/ decorator perhaps?
        if isinstance(number_type, ClientAPI):
            super().__init__(number, number_type)         # Actually meant to be an upper call
        else:
            self.number = number
            self.type = number_type


class CustomerAddress(BaseObject):
    _object_attributes = {
        "address_line_1": {"type": str, "ls_field": "address1"},
        "address_line_2": {"type": str, "ls_field": "address2"},
        "city": {"type": str, "ls_field": "city"},
        "state": {"type": str, "ls_field": "state"},
        "zipcode": {"type": str, "ls_field": "zip"},
        "country": {"type": str, "ls_field": "country"},
    }


class Customer(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customerID"},
        "first_name": {"type": str, "ls_field": "firstName"},
        "last_name": {"type": str, "ls_field": "lastName"},
        "name": {"combine": ["first_name", "last_name"]},
        "birthday": {"type": date, "ls_field": "dob", 'optional': True},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "title": {"type": str, "ls_field": "title"},
        "company": {"type": str, "ls_field": "company"},
        "company_registration_number": {"type": str, "ls_field": "companyRegistrationNumber"},
        "vat_number": {"type": str, "ls_field": "vatNumber"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "contact": {"type": 'Contact', 'optional': True, "ls_field": "Contact", "relationships": ["Contact"]},
        "tags": {"type": 'Tag', "multifield": True, "ls_field": "Tags.Tag", "relationships": ["Tags"]},
        "credit_account": {"type": 'CreditAccount', "ls_field": "CreditAccount", "ls_field_id": "creditAccountID", "relationships": ["CreditAccount"]},
        "type": {"type": 'CustomerType', "ls_field": "CustomerType", "ls_field_id": "customerTypeID", "relationships": ["CustomerType"]},
        "discount": {"type": 'Discount', "ls_field": "Discount", "ls_field_id": "discountID", "relationships": ["Discount"]},
        "tax_category": {"type": 'TaxCategory', "ls_field": "TaxCategory", "ls_field_id": "taxCategoryID", "relationships": ["TaxCategory"]},
        "note": {"type": 'Note', "ls_field": "Note", "relationships": ["Note"], 'optional': True},
        "custom_fields": {"type": 'CustomerCustomFieldValue', "multifield": True, "ls_field": "CustomFieldValues.CustomFieldValue", "relationships": ["CustomFieldValues", "CustomFieldValues.value"]},
    }
    _get_function = "CustomersAPI.get_customer"
    _update_url = 'Customer/%s.json'
    _create_url = 'Customer.json'
    
    def delete(self, anonymize=False):
        if anonymize:
            self.api.request('DELETE', f'Customer/{self.id}/Anonymize.json')
        else:
            self.api.request('DELETE', f'Customer/{self.id}.json')

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
