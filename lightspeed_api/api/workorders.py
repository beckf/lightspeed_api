
from . import BaseAPI
from ..models.workorder import *


class WorkordersAPI(BaseAPI):
    _all_methods = {
        "": {
            "url": "Workorder.json",
            "class": Workorder
        },
        "items": {
            "url": "WorkorderItem.json",
            "class": WorkorderItem
        },
        "lines": {
            "url": "WorkorderLine.json",
            "class": WorkorderLine
        },
        "statuses": {
            "url": "WorkorderStatus.json",
            "class": WorkorderStatus
        }
    }
    
    def get_workorder(self, id, preload_relations=[], raw=False):
        url = f'Workorder/{id}.json'
        return self._get_wrapper(url, raw=raw, preload_relations=preload_relations, object_class=Workorder)
    
    def get_workorder_item(self, id, preload_relations=[], raw=False):
        url = f'WorkorderItem/{id}.json'
        return self._get_wrapper(url, raw=raw, object_class=WorkorderItem) #, object_field='CustomField')
    
    def get_workorder_line(self, id, preload_relations=[], raw=False):
        url = f'WorkorderLine/{id}.json'
        return self._get_wrapper(url, raw=raw, object_class=WorkorderLine)
    
    def get_workorder_status(self, id, preload_relations=[], raw=False):
        url = f'WorkorderStatus/{id}.json'
        return self._get_wrapper(url, raw=raw, object_class=WorkorderStatus)