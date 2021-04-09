
from . import BaseAPI, BaseObject

class Tag(BaseObject):
    search_terms = {
        "id": {"type": int, "ls_field": "tagID", 'optional': True},
        "name": {"type": str, "ls_field": "name"}
    }
    get_function = ""           # TODO: implement
    # TODO: default values for optionals? So they can at least reference it?
    # TODO: when getting tags, they often don't have an ID value - what do we do then?
    # Do we build an auto-lookup function for this in particular? Or a "cleanup" function?
    # Do we do similar to the lazy attributes but for single items? And then it has to do different types of searching?
    
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