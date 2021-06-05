
from datetime import datetime

from . import BaseObject


class Category(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "categoryID"},
        "name": {"type": int, "ls_field": "name"},
        "created_time": {"type": int, "ls_field": "createTime"},
        "last_modified_time": {"type": int, "ls_field": "timeStamp"},
        "parent_category": {"type": 'Category', "ls_field": "Parent", "ls_field_id": "parentID", "relationships": ["Parent"]},
        "node_depth": {"type": str, "ls_field": "nodeDepth"},
        "full_path": {"type": str, "ls_field": "fullPathName"},
        "left_node": {"type": int, "ls_field": "leftNode"},
        "right_node": {"type": int, "ls_field": "rightNode"},
    }