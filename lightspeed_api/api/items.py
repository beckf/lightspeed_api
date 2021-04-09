
from datetime import datetime

from . import BaseAPI, BaseObject
from .tags import Tag

class Item(BaseObject):
    search_terms = {
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
        
        "emails": {"type": str, "multifield": True, "ls_field": "Contact.Emails.ContactEmail", "ls_secondary_field": "address", "relationships": ["Contact"]},
        "tags": {"type": Tag, "multifield": True, "ls_field": "Tags.Tag", "relationships": ["Tags"]},
        # TODO: make these map to objects dynamically instead of just an ID
        "category_id": {"type": int, "ls_field": "categoryID"},
        "item_matrix_id": {"type": int, "ls_field": "itemMatrixID"},
        "manufacturer_id": {"type": int, "ls_field": "manufacturerID"},
        "tax_class_id": {"type": int, "ls_field": "taxClassID"},
        "default_vendor_id": {"type": int, "ls_field": "defaultVendorID"},
        # TODO: Note field
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

class ItemsAPI(BaseAPI):
    def all(self, search=None, offset=0, last_modified=None):
        data = self.client.request('GET', f'Item.json?offset=%d' % offset)
        return_list = self._create_forever_list(data, Item, self.all)       # TODO: functools partial this.
        return return_list
    
    def get_item(self, ItemID):
        data = self.client.request('GET', f'Item/{ItemID}.json')
        if data is None or data['@attributes']['count'] == '0':
            return []
        
        return self._unwrap_object_to_cls(Item, data['Item'])

    # TODO: call tags API instead of doing it here.
    def get_tags_for_item(self, ItemID):
        data = self.client.request('GET', f'Item/{ItemID}.json?load_relations=["TagRelations.Tag"]')
        if data is None or data['@attributes']['count'] == '0':
            return []

        return_list = []
        tags = data['Item'].get('Tags', None)
        if tags:
            if type(tags['tag']) != list:
                return [tags['tag']]
            
            for obj in tags['tag']:
                return_list.append(self._unwrap_object_to_cls(Tag, obj))
        
        return return_list
    
    def get_items_with_tag(self, TagName):
        data = self.client.request('GET', f'Item.json?load_relations=["TagRelations.Tag", "TagRelations"]&Tags.tag={TagName}')
        if data is None or data['@attributes']['count'] == '0':
            return []
        
        # If there's only a single item in the return, it comes out
        # as a dict instead of a list. Convert it here.
        if type(data['Item']) == dict:
            data['Item'] = [data['Item']]
        
        return_list = []
        for obj in data['Item']:
            return_list.append(self._unwrap_object_to_cls(Item, obj))

        return return_list