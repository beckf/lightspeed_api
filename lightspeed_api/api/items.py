
from . import BaseAPI, BaseObject
from .tags import Tag

class Item(BaseObject):
    def __init__(self, obj=None, api=None):
        if obj:
            self.id = obj['itemID']
            self.created_at = obj['createTime']
            self.name = obj['description']
    
    @property
    def tags(self):
        return self.api.items.get_tags_for_item(self.id)
    
    def get_associated_sales(self, created_at=None):
        return self.api.sales.get_sales_for_item(self.id, created_at=created_at)

    def __repr__(self):
        return self.name

class ItemsAPI(BaseAPI):
    def get_item(self, ItemID):
        data = self.client.request('GET', f'Item/{ItemID}.json')
        if data is None or data['@attributes']['count'] == '0':
            return []
        
        return self._unwrap_sales_object(Item, data['Item'])

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
                return_list.append(self._unwrap_sales_object(Tag, obj))
        
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
            return_list.append(self._unwrap_sales_object(Item, obj))

        return return_list