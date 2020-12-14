
from . import BaseAPI, BaseObject

class Tag(BaseObject):
    def __init__(self, obj=None, api=None):
        if obj:
            self.id = obj['tagID']
            self.name = obj['name']
    
    @property
    def associated_items(self):
        return self.api.items.get_items_with_tag(self.name)
    
    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

class TagsAPI(BaseAPI):
    def all(self):
        data = self.client.request('GET', f'Tag.json')
        return_list = self._create_forever_list(data, Tag, self.all)       # TODO: functools partial this.
        return return_list