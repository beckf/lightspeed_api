
from datetime import datetime

from . import BaseObject


class Note(BaseObject):
    _object_attributes = {
        "text": {"type": str, "ls_field": "note"},
        "is_public": {"type": bool, "ls_field": "isPublic"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
    }