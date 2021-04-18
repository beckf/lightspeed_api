
from . import BaseAPI
from ..models.customer import Customer
from ..utils import search


class CustomersAPI(BaseAPI):
    @search(Customer)
    def all(self, search=None, offset=0, preload_relations=[]):
        url = f'Customer.json?offset=%d' % offset
        if search:
            url += "&" + search
        data = self.client.request('GET', url)
        return_list = self._create_forever_list(data, Customer, self.all, search, preload_relations)
        return return_list
    
    def get_customer(self, CustomerID, preload_relations=[], raw=False):
        url = f'Customer/{CustomerID}.json'
        if preload_relations:
            relations_str = '","'.join(preload_relations)
            url += f'?load_relations=["{relations_str}"]'
        print(url)
        data = self.client.request('GET', url)
        if raw:
            return data['Customer']
        return self._unwrap_object_to_cls(Customer, data['Customer'])
    
    # TODO: call tags API instead of doing it here.
    def get_tags_for_customer(self, CustomerID):
        data = self.client.request('GET', f'Customer/{CustomerID}.json?load_relations=["Tags"]')
        if data is None or data['@attributes']['count'] == '0':
            return []

        return_list = []
        tags = data['Customer'].get('Tags', None)
        if tags:
            if type(tags['Tag']) != list:
                return_list = [self._unwrap_object_to_cls(Tag, tags['Tag'])]
            else:
                for obj in tags['Tag']:
                    return_list.append(self._unwrap_object_to_cls(Tag, obj))
        
        return return_list