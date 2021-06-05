
from datetime import datetime
from . import BaseObject

class Manufacturer(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "manufacturerID"},
        "name": {"type": str, "ls_field": "name"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
    }