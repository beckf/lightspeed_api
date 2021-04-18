
from . import BaseAPI
from ..models.tag import Tag
from ..utils import search

class TagsAPI(BaseAPI):
    @search(Tag)
    def all(self, search=None, offset=0, preload_relations=[]):
        url = f'Tag.json?offset=%d' % offset
        if search:
            url += "&" + search
        data = self.client.request('GET', url)
        return_list = self._create_forever_list(data, Tag, self.all, search, preload_relations)
        return return_list

    def get_tag(self, TagID):
        url = f'Tag/{TagID}.json'
        data = self.client.request('GET', url)
        return self._unwrap_object_to_cls(Tag, data['Tag'])
