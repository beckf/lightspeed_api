
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
    
    def get_customer(self, id, preload_relations=[], raw=False):
        url = f'Customer/{id}.json'
        return self._get_wrapper(url, raw=raw, preload_relations=preload_relations, object_class=Customer)
    
    def get_customer_custom_field(self, id, preload_relations=[], raw=False):
        url = f'Customer/CustomField/{id}.json'
        return self._get_wrapper(url, raw=raw, object_class=CustomerCustomField, object_field='CustomField')
    
    def get_customer_type(self, id, preload_relations=[], raw=False):
        url = f'CustomerType/{id}.json'
        return self._get_wrapper(url, raw=raw, object_class=CustomerType)