
import json

from ..utils import convert_to_type, convert_from_type
from ..api import BaseAPI

# Lazy-loaded
API_MODULES = None
API_MODELS = None


def _get_model_class(class_name):
    global API_MODELS
    if not API_MODELS:
        API_MODELS = __import__('lightspeed_api').models
    return getattr(API_MODELS, class_name)


class BaseObject:
    def __init__(self, obj=None, api=None):
        self.api = api
        if obj:
            for term in self._object_attributes:
                ls_info = self._object_attributes[term]

                # Deal with combined fields later.
                if "combine" in ls_info:
                    continue
                
                try:
                    if "multifield" not in ls_info or not ls_info['multifield']:
                        if 'ls_field_id' in ls_info:
                            _id = int(obj[ls_info['ls_field_id']])
                            _class = ls_info['type']
                            if _id == 0:
                                data = None
                            else:
                                data = LazyLookupObject(_id, api, _class, self, term)
                        else:
                            obj_data = BaseObject._parse_field_parts(ls_info['ls_field'], obj, True)
                            if obj_data is None:
                                raise KeyError()       # triggers the relationships part below
                            if 'ls_secondary_field' in ls_info:
                                obj_data = obj_data[ls_info['ls_secondary_field']]
                            data = convert_to_type(ls_info['type'], obj_data)

                        if 'convert_class' in ls_info:
                            data = ls_info['convert_class'](data)

                        setattr(self, term, data)
                    else:
                        # It is a multi-field item.
                        data_list = BaseObject._parse_multifield(ls_info, obj, api)
                        if 'convert_class' in ls_info:
                            _data_list = []
                            for d in data_list:
                                _data_list.append(ls_info['convert_class'](d))
                            data_list = _data_list

                        if not data_list and "relationships" in ls_info:
                            setattr(self, term, LazyLookupAttributes(self.id, api, self._get_function, ls_info))
                        else:
                            setattr(self, term, data_list)
                except KeyError as ex:
                    if not ('optional' in ls_info and ls_info['optional']):
                        raise ex
                    elif 'relationships' in ls_info:
                        # Optional, but an object to be loaded - put it as a LazyLookupAttributes
                        setattr(self, term, LazyLookupAttributes(self.id, api, self._get_function, ls_info))
                    else:
                        setattr(self, term, ls_info.get('default', None))
            
            for term in self._object_attributes:
                ls_info = self._object_attributes[term]

                # Only dealing with combined fields now
                if "combine" not in ls_info:
                    continue

                values = []
                for attr in ls_info['combine']:
                    values.append(getattr(self, attr))

                setattr(self, term, " ".join(values))

            # Run the "cleanup" function if specified.
            # Used to make some last-minute queries/adjustments if needed.
            _cleanup = getattr(self, 'cleanup', None)
            if _cleanup and callable(_cleanup):
                _cleanup()

        else:
            for term in self._object_attributes:
                ls_info = self._object_attributes[term]
                data = None

                if "multifield" in ls_info and ls_info['multifield']:
                    data = []

                data = ls_info.get('default', data)
                setattr(self, term, data)

    @staticmethod
    def _parse_field_parts(ls_field, obj, notlist=False):
        parts = ls_field.split('.')
        downstream_obj = obj
        for p in parts:
            # This happens when there is no data - a list/dict becomes an empty string.
            # If so, we'll exit out and assume there is no data.
            if type(downstream_obj) == str or p not in downstream_obj:
                downstream_obj = [] if not notlist else None
                break
            downstream_obj = downstream_obj[p]
        
        return downstream_obj

    @staticmethod
    def _parse_multifield(ls_info, obj, api):
        data_list = []
        downstream_obj = BaseObject._parse_field_parts(ls_info['ls_field'], obj)

        second_field = None
        if 'ls_secondary_field' in ls_info:
            second_field = ls_info['ls_secondary_field']

        # Only a single element in the "list"
        if type(downstream_obj) == dict:
            downstream_obj = [downstream_obj]

        for item in downstream_obj:
            if second_field:
                data = convert_to_type(ls_info['type'], item[second_field])
            elif type(ls_info['type']) == str:          # Means it's an object/class
                _class = _get_model_class(ls_info['type'])
                data = _class(item, api)
            else:
                raise Exception("Unexpected combination - multifield item, no ls_secondary_field or typecasting")
            data_list.append(data)

        return data_list
    
    def json(self, dump=True):
        obj = {}
        for term in self._object_attributes:
            ls_info = self._object_attributes[term]

            # Ignore combined fields
            if "combine" in ls_info:
                continue
            
            field = ls_info.get('ls_field', ls_info.get('ls_field_id', None))
            _obj = obj
            if len(field.split(".")) > 1:
                fields = field.split(".")
                # This is a nested object, so we'll want to go down the rabbit hole until we get there.
                for f in fields:
                    if f not in _obj:
                        _obj[f] = {}
                    
                    # Go down the object as you get each field.
                    # Don't do this the last time - we'll be where we want to be.
                    # ^ EXCEPTION: if ls_secondary_field is set, do actually go down the object one last time.
                    if fields[-1] != f:
                        _obj = _obj[f]
                    elif 'ls_secondary_field' in ls_info:
                        _obj = _obj[f]
                    
                    field = f       # Last one we put here will be the actual field to use.
                
                if 'ls_secondary_field' in ls_info:
                    field = ls_info['ls_secondary_field']
            
            if "multifield" not in ls_info or not ls_info['multifield']:
                data = getattr(self, term)
                if data:
                    if 'ls_field_id' in ls_info:
                        field = ls_info['ls_field_id']
                        # TODO: determine if data needs to be saved before continuing.
                        data = data.id
                    else:
                        data = convert_from_type(ls_info['type'], data)
                    _obj[field] = data
            else:
                # It is a multi-field item.
                data_list = getattr(self, term)
                if data_list:
                    converted_data_list = []
                    for d in data_list:
                        dc = convert_from_type(ls_info['type'], d)
                        converted_data_list.append(dc)
                    
                    _obj[field] = converted_data_list
        
        return json.dumps(obj) if dump else obj
    
    def set_api(self, api):
        self.api = api
    
    def save(self):
        if self.id:
            url = getattr(self, '_update_url', None)
            if url:
                self.api.request('PUT', url % self.id, self.json())
            else:
                raise Exception("Unable to save changes of this object type - API doesn't handle it.")
        else:
            url = getattr(self, '_create_url', None)
            if url:
                response = self.api.request('POST', url, self.json())
            else:
                raise Exception("Unable to create objects of this type - API doesn't handle it.")
            
            if not response:
                raise Exception("No object returned from Lightspeed - invalid object creation attempted.")
            
            response.pop('@attributes')
            key = list(response.keys())[0]
            self.id = response[key][self._object_attributes['id']['ls_field']]
    
    def delete(self):
        raise Exception("Cannot delete this object type - API doesn't handle it.")

    def __eq__(self, item):
        if type(item) in [type(self), LazyLookupObject]:
            if 'id' not in self._object_attributes or not getattr(item, 'id', None):
                return self.json() == item.json()
            return item.id == self.id
        return super().__eq__(item)



class LazyLookupObject:
    def __init__(self, id, client, class_obj, parent_obj, parent_field):
        self.id = id
        self._client = client
        self._class_obj = _get_model_class(class_obj)
        self._parent_obj = parent_obj
        self._parent_field = parent_field
        self._was_loaded = False
    
    def _load(self):
        global API_MODULES
        if not API_MODULES:
            API_MODULES = __import__('lightspeed_api').api

        if not self._was_loaded:
            parts = self._class_obj._get_function.split('.')
            resolved_function = getattr(API_MODULES, parts[0])
            for p in parts[1:]:
                resolved_function = getattr(resolved_function, p)
            
            if not callable(resolved_function):
                raise Exception("Cannot resolve function '%s'" % self._func)
            
            api = BaseAPI(self._client)
            data = resolved_function(api, self.id)
            setattr(self._parent_obj, self._parent_field, data)
            self._was_loaded = True

    def __getattr__(self, attr):
        if attr != '_was_loaded':
            if '_was_loaded' in self.__dict__ and not self.__dict__['_was_loaded']:
                self._load()
                return getattr(getattr(self._parent_obj, self._parent_field), attr)
        
        return self.__dict__[attr]
    
    def __setattr__(self, attr, val):
        if attr != '_was_loaded':
            if '_was_loaded' in self.__dict__ and not self.__dict__['_was_loaded']:
                self._load()
                return setattr(getattr(self._parent_obj, self._parent_field), attr, val)
        
        return super().__setattr__(attr, val)



class LazyLookupAttributes:
    def __init__(self, id, client, func, ls_info):
        self._id = id
        self._client = client
        self._func = func
        self._list = []
        self._ls_info = ls_info
        self._was_loaded = False
    
    def _load(self):
        global API_MODULES
        if not API_MODULES:
            API_MODULES = __import__('lightspeed_api').api
        
        if not self._was_loaded:
            parts = self._func.split('.')
            resolved_api_module = getattr(API_MODULES, parts[0])
            resolved_function = resolved_api_module
            for p in parts[1:]:
                resolved_function = getattr(resolved_function, p)
            
            if not callable(resolved_function):
                raise Exception("Cannot resolve function '%s'" % self._func)
            
            relations = self._ls_info['relationships']
            api = resolved_api_module(self._client)
            data = resolved_function(api, self._id, preload_relations=relations, raw=True)
            self._list = BaseObject._parse_multifield(self._ls_info, data, self._client)
            self._was_loaded = True

    def __getattr__(self, attr):
        if attr in ["_id", "_client", "_func", "_list", "_ls_info", "_was_loaded"]:
            return self.__dict__[attr]

        if not self._was_loaded:
            self._load()

        if len(self._list) != 1:
            raise Exception("Cannot access attribute of list object for field %s" % attr)
        else:
            return getattr(self._list[0], attr)
    
    def __setattr__(self, attr, val):
        if attr in ["_id", "_client", "_func", "_list", "_ls_info", "_was_loaded"]:
            return super().__setattr__(attr, val)

        if not self._was_loaded:
            self._load()

        if len(self._list) != 1:
            raise Exception("Cannot set attribute of list object for field %s" % attr)
        else:
            return setattr(self._list[0], attr, val)
        
        return super().__setattr__(attr, val)

    def __getitem__(self, key):
        self._load()
        return self._list[key]
    
    def __len__(self):
        self._load()
        return len(self._list)
    
    def __repr__(self):
        self._load()
        if 'multifield' not in self._list:
            if len(self._list) == 0:
                return None
            return self._list[0]
        return str(self._list)
    
    def __eq__(self, item):
        self._load()
        if 'multifield' not in self._ls_info:
            return item == self._list[0]
        return item == self._list


# Done after declaring the above class
from .catalog import *
from .category import *
from .contact import *
from .credit_account import *
from .credit_card import *
from .customer import *
from .discount import *
from .employee import *
from .image import *
from .industry import *
from .inventory import *
from .item import *
from .locale import *
from .note import *
from .manufacturer import *
from .options import *
from .order import *
from .payment_type import *
from .price_level import *
from .register import *
from .sale import *
from .serialized import *
from .session import *
from .shipping import *
from .shop import *
from .tag import *
from .tax import *
from .vendor import *
from .workorder import *
