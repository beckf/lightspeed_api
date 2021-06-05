
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
        "is_taxed": {"type": bool, "ls_field": "tax"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "is_discountable": {"type": bool, "ls_field": "discountable"},
        "is_serialized": {"type": bool, "ls_field": "serialized"},
        "is_publishable_to_ecom": {"type": bool, "ls_field": "publishToEcom"},
        "type": {"type": str, "ls_field": "systemSku"},     # TODO: handle enum values: default, non_inventory, serialized, box, serialized_assembly, assembly
        "description": {"type": str, "ls_field": "description"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "tags": {"type": Tag, "multifield": True, "ls_field": "Tags.tag", "relationships": ["TagRelations.Tag"]},
        "category": {"type": 'Category', "ls_field": "categoryID", "relationships": ["Category"]},
        "item_matrix": {"type": 'ItemMatrix', "ls_field": "itemMatrixID"},
        "manufacturer": {"type": 'Manufacturer', "ls_field": "manufacturerID", "relationships": ["Manufacturer"]},
        "tax_class": {"type": 'TaxClass', "ls_field": "taxClassID", "relationships": ["TaxClass"]},
        "default_vendor": {"type": "Vendor", "ls_field": "defaultVendorID"},
        # TODO: Images, ItemAttributes, ItemShops, ItemComponents, ItemShelfLocations, ItemVendorNums fields
        "note": {"type": 'Note', "ls_field": "Note", "relationships": ["Note"], 'optional': True},
        "custom_fields": {"type": 'ItemCustomFieldValue', "multifield": True, "ls_field": "CustomFieldValues.CustomFieldValue", "relationships": ["CustomFieldValues", "CustomFieldValues.value"]},
    }

    def get_associated_sales(self, created_at=None):
        return self.api.sales.get_sales_for_item(self.id, created_at=created_at)

    def __repr__(self):
        return self.name

    # TODO: get_image function

class ItemCustomField(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
        "name": {"type": str, "ls_field": "name"},
        "type": {"type": str, "ls_field": "type"},
        "units": {"type": str, "ls_field": "uom"},
        "decimal_precision": {"type": int, "ls_field": "decimalPrecision"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "default": {"type": str, "ls_field": "default"},    # TODO: may be a mixed type, so this may not work?
    }


class ItemCustomFieldValue(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldValueID"},
        "custom_field": {"type": 'ItemCustomField', "ls_field_id": "customFieldID"},
        "is_deleted": {"type": bool, "ls_field": "deleted"},
        "name": {"type": str, "ls_field": "name"},
        "type": {"type": str, "ls_field": "type"},      # TODO: do we want to convert this to a Python type?
        "value": {"type": str, "ls_field": "value"},    # TODO: do we want to convert this to its Python type?
    }


class ItemCustomFieldChoice(BaseObject):
    _object_attributes = {      # TODO: same as customer?
        "id": {"type": int, "ls_field": "customFieldChoiceID"},
        "name": {"type": str, "ls_field": "name"},
        "value": {"type": str, "ls_field": "value"},
        "is_deletable": {"type": bool, "ls_field": "canBeDeleted"},
        "custom_field": {"type": 'ItemCustomField', "ls_field_id": "customFieldID"},
    }


class ItemAttributeSet(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "itemAttributeSetID"},
        "name": {"type": str, "ls_field": "name"},
        "attribute_1": {"type": str, "ls_field": "attributeName1"},
        "attribute_2": {"type": str, "ls_field": "attributeName2"},
        "attribute_3": {"type": str, "ls_field": "attributeName3"},
    }


class ItemMatrix(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "itemMatrixID"},
        "default_cost": {"type": float, "ls_field": "defaultCost"},
        "is_taxed": {"type": bool, "ls_field": "tax"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "is_serialized": {"type": bool, "ls_field": "serialized"},
        "type": {"type": str, "ls_field": "systemSku"},     # TODO: handle enum values: default, non_inventory, serialized, box, serialized_assembly, assembly
        "description": {"type": str, "ls_field": "description"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "category": {"type": 'Category', "ls_field": "categoryID", "relationships": ["Category"]},
        "manufacturer": {"type": 'Manufacturer', "ls_field": "manufacturerID", "relationships": ["Manufacturer"]},
        "tax_class": {"type": 'TaxClass', "ls_field": "taxClassID", "relationships": ["TaxClass"]},
        "default_vendor": {"type": "Vendor", "ls_field": "defaultVendorID"},
        "item_attributes": {"type": 'ItemAttributeSet', "ls_field": "itemAttributeSetID", "relationships": ["ItemAttributeSet"]},
        "items": {"type": 'Item', "multifield": True, "ls_field": "Items.Item", "relationships": ["Items"]},
        "custom_fields": {"type": 'ItemCustomFieldValue', "multifield": True, "ls_field": "CustomFieldValues.CustomFieldValue", "relationships": ["CustomFieldValues", "CustomFieldValues.value"]},
    }
    # TODO: images attribute