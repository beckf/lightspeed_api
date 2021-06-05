
from datetime import datetime
from . import BaseObject

class TaxCategory(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "taxCategoryID"},
        "is_tax_inclusive": {"type": bool, "ls_field": "isTaxInclusive"},
        "tax_name_1": {"type": str, "ls_field": "tax1Name"},
        "tax_name_2": {"type": str, "ls_field": "tax2Name"},
        "tax_rate_1": {"type": float, "ls_field": "tax1Rate"},
        "tax_rate_2": {"type": float, "ls_field": "tax2Rate"},
        "tax_classes": {"type": 'TaxCategoryClass', "multifield": True, "ls_field": "TaxCategoryClasses.TaxCategoryClass", "relationships": ["TaxCategoryClasses", "TaxCategoryClasses.TaxClass"]},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
    }


class TaxCategoryClass(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "taxCategoryClassID"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
    }


class TaxClass(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "taxClassID"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "name": {"type": str, "ls_field": "name"},
    }