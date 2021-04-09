
from ..utils import convert_to_type

class BaseAPI:
    def __init__(self, client):
        self.client = client
    
    def _unwrap_object_to_cls(self, objcls, obj):
        return objcls(obj, api=self.client)
    
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

        self.account_id = self.account.get_account_id()
    
    def request(self, req_type, url, data=None):
        if not url.startswith("http"):
            url = f"https://api.lightspeedapp.com/API/Account/{self.account_id}/" + url

        return self.client.request_bucket(req_type, url, data=data)
    
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


class BaseObject:
    def __init__(self, obj=None, api=None):
        self.api = api
        if obj:
            # TODO: do back-and-forth functions...
            # do we just build the one func to convert python<->lsfield ?
            for term in self.search_terms:
                ls_info = self.search_terms[term]

                # Deal with combined fields later.
                if "combine" in ls_info:
                    continue
                
                try:
                    if "multifield" not in ls_info or not ls_info['multifield']:
                        data = convert_to_type(ls_info['type'], obj[ls_info['ls_field']])
                        setattr(self, term, data)
                    else:
                        # It is a multi-field item.
                        data_list = BaseObject._parse_multifield(ls_info, obj, api)
                        
                        if data_list:
                            setattr(self, term, data_list)
                        else:
                            setattr(self, term, LazyLookupAttributes(self.id, api, self.get_function, ls_info))
                    
                    # TODO: remove. This is a temporary debugging tool
                    if 'optional' in ls_info and ls_info['optional']:
                        print('OPTIONAL FIELD FOUND: ', obj)
                except KeyError as ex:
                    if not ('optional' in ls_info and ls_info['optional']):
                        raise ex
            
            for term in self.search_terms:
                ls_info = self.search_terms[term]

                # Only dealing with combined fields now
                if "combine" not in ls_info:
                    continue
                
                values = []
                for attr in ls_info['combine']:
                    values.append(getattr(self, attr))
                
                setattr(self, term, " ".join(values))

    @staticmethod
    def _parse_multifield(ls_info, obj, api):
        data_list = []
        parts = ls_info['ls_field'].split('.')
        downstream_obj = obj
        for p in parts:
            # This happens when there is no data - a list/dict becomes an empty string.
            # If so, we'll exit out and assume there is no data.
            if type(downstream_obj) == str or p not in downstream_obj:
                downstream_obj = []
                break
            downstream_obj = downstream_obj[p]
        
        second_field = None
        if 'ls_secondary_field' in ls_info:
            second_field = ls_info['ls_secondary_field']
        
        # Only a single element in the "list"
        if type(downstream_obj) == dict:
            downstream_obj = [downstream_obj]
        
        for item in downstream_obj:
            if second_field:
                data = convert_to_type(ls_info['type'], item[second_field])
            elif issubclass(ls_info['type'], BaseObject):
                data = ls_info['type'](item, api)
            else:
                raise Exception("Unexpected combination - multifield item, no ls_secondary_field or typecasting")
            data_list.append(data)

        return data_list

    def get_search_string(self, args):
        for arg in args:
            ls_field = self.search_terms[arg]
    
    def json(self):
        return self.json_object


class LazyLookupAttributes:
    def __init__(self, id, client, func, ls_info):
        self.id = id
        self.client = client
        self.func = func
        self.list = []
        self.ls_info = ls_info
    
    def _load(self):
        if not self.list:
            parts = self.func.split('.')
            resolved_function = globals().get(parts[0])
            for p in parts[1:]:
                resolved_function = getattr(resolved_function, p)
            
            if not callable(resolved_function):
                raise Exception("Cannot resolve function '%s'" % self.func)
            
            relations = self.ls_info['relationships']
            api = BaseAPI(self.client)
            data = resolved_function(api, self.id, preload_relations=relations, raw=True)
            self.list = BaseObject._parse_multifield(self.ls_info, data, self.client)

    def __getitem__(self, key):
        self._load()
        return self.list[key]
    
    def __len__(self):
        self._load()
        return len(self.list)
    
    def __repr__(self):
        self._load()
        return str(self.list)


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