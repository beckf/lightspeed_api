
from . import BaseAPI
from ..models.vendor import *


class VendorsAPI(BaseAPI):
    _all_methods = {
        "": {
            "url": "Vendor.json",
            "class": Vendor
        }
    }
    
    def get_vendor(self, id, preload_relations=[], raw=False):
        url = f'Vendor/{id}.json'
        return self._get_wrapper(url, raw=raw, preload_relations=preload_relations, object_class=Vendor)
