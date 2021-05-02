
from . import BaseAPI
from ..models.item import Item


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