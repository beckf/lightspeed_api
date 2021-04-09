
from datetime import datetime

from ..utils import search
from . import BaseAPI, BaseObject
from .tags import Tag


class Customer(BaseObject):
    # TODO: change to be "object_attributes" or something...
    search_terms = {
        "id": {"type": int, "ls_field": "customerID"},
        "first_name": {"type": str, "ls_field": "firstName"},
        "last_name": {"type": str, "ls_field": "lastName"},
        "name": {"combine": ["first_name", "last_name"]},
        "birthday": {"type": datetime, "ls_field": "dob", 'optional': True},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "title": {"type": str, "ls_field": "title"},
        "company": {"type": str, "ls_field": "company"},
        "company_registration_number": {"type": str, "ls_field": "companyRegistrationNumber"},
        "vat_number": {"type": str, "ls_field": "vatNumber"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "emails": {"type": str, "multifield": True, "ls_field": "Contact.Emails.ContactEmail", "ls_secondary_field": "address", "relationships": ["Contact"]},
        "tags": {"type": Tag, "multifield": True, "ls_field": "Tags.Tag", "relationships": ["Tags"]},
        # TODO: make these map to objects dynamically instead of just an ID
        "credit_account_id": {"type": int, "ls_field": "creditAccountID"},
        "customer_type_id": {"type": int, "ls_field": "customerTypeID"},
        "discount_id": {"type": int, "ls_field": "discountID"},
        "tax_category_id": {"type": int, "ls_field": "taxCategoryID"},
        # TODO: Note field
        # TODO: CustomFieldValues field
    }
    get_function = "CustomersAPI.get_customer"
    
    def save(self):
        if self.id:
            self.api.client.request('PUT', f'Customer/{self.id}.json', self)
        else:
            response = self.api.client.request('POST', f'Customer/{self.id}.json', self)
            self.id = response["Customer"][self.search_terms['id']['ls_field']]

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


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