
from . import BaseAPI, BaseObject

class Customer(BaseObject):
    def __init__(self, obj=None, api=None):
        if obj:
            self.id = obj['customerID']
            self.name = obj['firstName'] + ' ' + obj['lastName']
            self.firstname = obj['firstName']
            self.lastname = obj['lastName']
            self.email = obj['Contact']['Emails']['ContactEmail']['address'] if obj['Contact']['Emails'] else ''
    
    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

class CustomersAPI(BaseAPI):
    def all(self):
        data = self.client.request('GET', f'Customer.json')
        return_list = self._create_forever_list(data, Customer, self.all)       # TODO: functools partial this.
        return return_list
    
    def get_customer(self, CustomerID):
        data = self.client.request('GET', f'Customer/{CustomerID}.json?load_relations=["Contact"]')
        if data is None:
            return []
        
        return self._unwrap_sales_object(Customer, data['Customer'])