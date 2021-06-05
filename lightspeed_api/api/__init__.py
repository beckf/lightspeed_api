
import functools

from ..utils import convert_to_type, search


class BaseAPI:
    def __init__(self, client):
        self.client = client
        if getattr(self, '_all_methods', None):
            for _obj_name in self._all_methods.keys():
                obj = self._all_methods[_obj_name]
                _name = 'all' if _obj_name == "" else 'all_%s' % _obj_name
                _url = obj['url']
                _class_obj = obj['class']
                setattr(self, _name, search(_class_obj)(functools.partial(self._all_wrapper, _url, _class_obj)))
    
    def _unwrap_object_to_cls(self, objcls, obj):
        return objcls(obj, api=self.client)
    
    def _all_wrapper(self, _all_url, _class_obj, search=None, offset=0, preload_relations=[]):
        url = f'%s?offset=%d' % (_all_url, offset)
        if search:
            url += "&" + search
        data = self.client.request('GET', url)
        return_list = self._create_forever_list(data, _class_obj, functools.partial(self._all_wrapper, _all_url, _class_obj), search, preload_relations)
        return return_list
    
    def _get_wrapper(self, url, raw=False, preload_relations=[], object_class=None, object_field=None):
        if preload_relations:
            relations_str = '","'.join(preload_relations)
            url += f'?load_relations=["{relations_str}"]'
        data = self.client.request('GET', url)
        
        # TODO: figure out how this'll work without that _class_obj field
        data_fieldname = object_class.__name__
        data_object_class = object_class
        if object_field:
            data_fieldname = object_field
        
        if raw:
            return data[data_fieldname]
        if not data:
            return None
        return self._unwrap_object_to_cls(data_object_class, data[data_fieldname])
    
    def _create_forever_list(self, data, objcls, retrieval_func, search, preload_relations):
        return_list = []
        if len(data.keys()) != 2:
            return []       # Probably at the end of the list
        
        _metadata = data.pop('@attributes')
        item_count = int(_metadata['count'])
        offset = int(_metadata['offset'])
        limit = int(_metadata['limit'])

        if item_count == 1:
            return_list.append(self._unwrap_object_to_cls(objcls, data[list(data.keys())[0]]))
        else:
            for obj in data[list(data.keys())[0]]:        # Since there's only 2 keys in the data dict at this point.
                return_list.append(self._unwrap_object_to_cls(objcls, obj))

        last_record_count = (offset + 1) * limit
        if item_count > last_record_count:
            # Create the "infinite list" object
            return_list = LazyLookupList(return_list, retrieval_func, item_count, search, preload_relations)

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
        self.registers_api = RegistersAPI(self)
        self.workorders_api = WorkordersAPI(self)
        self.vendors_api = VendorsAPI(self)

        self.account_id = self.account.get_account_id()
    
    def request(self, req_type, url, data=None):
        if not url.startswith("http"):
            url = f"https://api.lightspeedapp.com/API/Account/{self.account_id}/" + url

        return self.client.request_bucket(req_type, url, data=data)
    
    def add(self, obj):
        obj.set_api(self)

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
        return self.registers_api

    @property
    def customers(self):
        return self.customers_api
    
    @property
    def employees(self):
        return None
    
    @property
    def orders(self):
        return None
    
    @property
    def vendors(self):
        return self.vendors_api

    @property
    def workorders(self):
        return self.workorders_api


class LazyLookupList:
    def __init__(self, cur_list, func, total_count, search, preload_relations):
        self.func = func
        self.list = cur_list
        self.total_count = total_count
        self.search = search
        self.preload_relations = preload_relations
    
    def __getitem__(self, key):
        while key >= len(self.list) and (len(self.list) < self.total_count or self.total_count == 0):
            extra = self.func(offset=len(self.list),
                              search=self.search,
                              preload_relations=self.preload_relations)
            if len(extra) == 0:
                self.total_count = len(self.list)
            self.list.extend(extra.list if type(extra) == LazyLookupList else extra)
        
        return self.list[key]
    
    def __len__(self):
        return self.total_count


# Done after declaring the above class
from .sales import SalesAPI
from .items import ItemsAPI
from .accounts import AccountsAPI
from .tags import TagsAPI
from .customers import CustomersAPI
from .registers import RegistersAPI
from .workorders import WorkordersAPI
from .vendors import VendorsAPI