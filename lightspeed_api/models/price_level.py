
from . import BaseObject

class PriceLevel(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "priceLevelID"},
        "name": {"type": str, "ls_field": "name"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "can_be_archived": {"type": bool, "ls_field": "canBeArchived"},
        "type": {"type": int, "ls_field": "type"},      # TODO: enum
        "calculation": {"type": str, "ls_field": "Calculation"},        # TODO: "reference" type?
    }