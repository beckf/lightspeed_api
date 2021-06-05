
from . import BaseObject

class Tag(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "tagID", 'optional': True, 'default': 0},
        "name": {"type": str, "ls_field": "name"}
    }
    _get_function = "TagsAPI.get_tag"
    _update_url = 'Customer/%s.json'
    _create_url = 'Customer.json'
    
    def cleanup(self):
        if self.id == 0:
            _tags = self.api.tags.all(name=self.name)
            if _tags and len(_tags) == 1:
                self.id = _tags[0].id

    @property
    def associated_items(self):
        return self.api.items.get_items_with_tag(self.name)
    
    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, item):
        return self.id == item.id if item.id and self.id else self.name == item.name 


# TODO: explore this a bit more before we go do it
# Unsure of what it will do/have (it's an XML format?)
class TagGroup(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "customFieldID"},
    }
