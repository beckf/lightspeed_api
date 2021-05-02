
from . import BaseAPI
from ..models.customer import *


class CustomersAPI(BaseAPI):
    _all_methods = {
        "": {
            "url": "Customer.json",
            "class": Customer
        },
        "customer_custom_fields": {
            "url": "Customer/CustomField.json",
            "class": CustomerCustomField
        },
        "customer_types": {
            "url": "CustomerType.json",
            "class": CustomerType
        }
    }
    
    def get_customer(self, CustomerID, preload_relations=[], raw=False):
        url = f'Customer/{CustomerID}.json'
        return self._get_wrapper(url, raw=raw, preload_relations=preload_relations, object_class=Customer)
    
    def get_customer_custom_field(self, CustomFieldID, raw=False):
        url = f'Customer/CustomField/{CustomFieldID}.json'
        return self._get_wrapper(url, raw=raw, object_class=CustomerCustomField, object_field='CustomField')
    
    def get_customer_type(self, CustomerTypeID, raw=False):
        url = f'CustomerType/{CustomerTypeID}.json'
        return self._get_wrapper(url, raw=raw, object_class=CustomerType)