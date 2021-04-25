
from datetime import datetime
from . import BaseObject
from .tag import Tag


class Item(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "itemID"},
        "sku": {"type": str, "ls_field": "systemSku"},
        "upc": {"type": str, "ls_field": "upc"},
        "ean": {"type": str, "ls_field": "ean"},
        "custom_sku": {"type": str, "ls_field": "customSku"},
        "manufacturer_sku": {"type": str, "ls_field": "manufacturerSku"},
        "default_cost": {"type": float, "ls_field": "defaultCost"},
        "average_cost": {"type": float, "ls_field": "avgCost"},
        "taxed": {"type": bool, "ls_field": "tax"},
        "archived": {"type": bool, "ls_field": "archived"},
        "discountable": {"type": bool, "ls_field": "discountable"},
        "serialized": {"type": bool, "ls_field": "serialized"},
        "added_to_ecom": {"type": bool, "ls_field": "publishToEcom"},
        "type": {"type": str, "ls_field": "systemSku"},     # TODO: handle enum values: default, non_inventory, serialized, box, serialized_assembly, assembly
        "description": {"type": str, "ls_field": "description"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "tags": {"type": Tag, "multifield": True, "ls_field": "Tags.tag", "relationships": ["TagRelations.Tag"]},
        # TODO: make these map to objects dynamically instead of just an ID
        "category_id": {"type": int, "ls_field": "categoryID"},
        "item_matrix_id": {"type": int, "ls_field": "itemMatrixID"},
        "manufacturer_id": {"type": int, "ls_field": "manufacturerID"},
        "tax_class_id": {"type": int, "ls_field": "taxClassID"},
        "default_vendor_id": {"type": int, "ls_field": "defaultVendorID"},
        # TODO: Note field
        # TODO: Category, TaxClass, ItemAttributes, Manufacturer, ItemShops,
        #       ItemComponents, ItemShelfLocations, ItemVendorNums fields
        # TODO: CustomFieldValues field
    }
    def __init__(self, obj=None, api=None):
        if obj:
            # TODO: figure out if fields (like self.name) are just references to fields in the JSON blob or extracted as-is
            self.id = obj['itemID']
            self.created_at = obj['createTime']
            self.name = obj['description']
            self.tags = []
            self.json_object = obj
    
    # TODO: move this + setter into BaseObject
    # TODO: setter function should have format function to set up the object (i.e. converting from str to obj)?
    @property
    def tags(self):
        if not self._tags:
            self._tags = self.api.items.get_tags_for_item(self.id)
        return self._tags        # TODO: return list object that allows you to add/delete from the list via just a string (instead of a tag object)?
    
    @tags.setter
    def tags(self, tags):
        self._tags = []
        for t in tags:
            self._tags.append(Tag({"name": t, "tagID": None}))

    def get_associated_sales(self, created_at=None):
        return self.api.sales.get_sales_for_item(self.id, created_at=created_at)

    def __repr__(self):
        return self.name


class ItemCustomField(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }


class ItemCustomFieldChoice(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }


class ItemAttributeSet(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }


class ItemMatrix(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }