
class BaseAPI:
    def __init__(self, client):
        self.client = client
    
    def _unwrap_sales_object(self, objcls, obj):
        o = objcls(obj)
        o.set_api(self.client)
        return o
    
    def _create_forever_list(self, data, objcls, retrieval_func):
        return_list = []
        if len(data.keys()) != 2:
            print("ruh roh, this doesn't make sense!")
        
        _metadata = data.pop('@attributes')
        for obj in data[list(data.keys())[0]]:        # Since there's only 2 ever.
            return_list.append(self._unwrap_sales_object(objcls, obj))

        last_record_count = (int(_metadata['offset']) + 1) * int(_metadata['limit'])
        if int(_metadata['count']) > last_record_count:
            # Create the "infinite list" object
            return_list = LazyLookupList(return_list, retrieval_func)

        return return_list


class ClientAPI:
    def __init__(self, client):
        self.client = client

        # In order to reduce memory costs for running
        # multiple instances of each API per client, I'm
        # using instances of the APIs accordingly.
        self.accounts_api = AccountsAPI(self)
        self.sales_api = SalesAPI(self)
        self.items_api = ItemsAPI(self)
        self.tags_api = TagsAPI(self)
        self.customers_api = CustomersAPI(self)

        self.account_id = self.account.get_account_id()
    
    def request(self, req_type, url):
        if not url.startswith("http"):
            url = f"https://api.lightspeedapp.com/API/Account/{self.account_id}/" + url

        return self.client.request_bucket(req_type, url)
    
    @property
    def account(self):
        return self.accounts_api
    
    @property
    def sales(self):
        return self.sales_api
    
    @property
    def items(self):
        return self.items_api
    
    @property
    def tags(self):
        return self.tags_api

    @property
    def inventory(self):
        return None
    
    @property
    def registers(self):
        return None

    @property
    def customers(self):
        return self.customers_api
    
    @property
    def employees(self):
        return None
    
    @property
    def orders(self):
        return None


class BaseObject:
    def set_api(self, api):
        self.api = api


class LazyLookupList:
    def __init__(self, cur_list, func):
        self.func = func
        self.list = cur_list
    
    def __getitem__(self, key):
        if key >= len(self.list):
            extra = self.func(key)
            self.list.extend(extra)
        
        return self.list[key]


# Done after declaring the above class
from .sales import SalesAPI
from .items import ItemsAPI
from .accounts import AccountsAPI
from .tags import TagsAPI
from .customers import CustomersAPI