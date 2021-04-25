
from datetime import datetime, date

LIGHTSPEED_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S+00:00"


# Checks if the type can be converted from it's current type to the given type
# Usually specific to dates, integers and lists.
def convert_to_type(obj_type, obj):
    if obj_type == str:
        return obj
    elif obj_type == bool:
        if obj.lower() in ["true", "false"]:
            return obj == "true"
        else:
            raise Exception("The value %s could not be converted to a boolean value" % obj)
    elif obj_type == int:
        try:
            return int(obj)
        except ValueError:
            raise Exception("The value %s could not be converted to a number" % obj)
    elif obj_type == datetime:
        try:
            dtobj = datetime.strptime(obj, LIGHTSPEED_DATETIME_FORMAT)
        except ValueError:
            raise Exception("The value %s could not be converted to a date/time" % obj)
        return dtobj
    elif obj_type == date:
        try:
            dtobj = datetime.strptime(obj, LIGHTSPEED_DATETIME_FORMAT).date()
        except ValueError:
            raise Exception("The value %s could not be converted to a date" % obj)
        return dtobj
    
    # All other cases just fall back to original data
    return obj


def convert_from_type(obj_type, obj):
    if obj_type == str:
        return str(obj)         # Done to force conversion of Object to str if applicable
    elif obj_type == int:
        return str(obj)
    elif obj_type in [datetime, date]:
        try:
            dtobj = datetime.strftime(obj, LIGHTSPEED_DATETIME_FORMAT)
        except ValueError:
            raise Exception("The value %s could not be converted from a date/time object to a string" % obj)
        return dtobj
    elif isinstance(obj, object):
        return obj.json(dump=False)
    
    # All other cases just fall back to original data
    return obj


def get_search_string(search_terms, args_dict):
    search = ""
    for term in args_dict:
        ls_info = search_terms[term]
        if callable(args_dict[term]):
            search += "&" + args_dict[term](ls_info['ls_field'])
        else:
            search += f"&{ls_info['ls_field']}={args_dict[term]}"
    
    print("SEARCH: ", search[1:])
    return search[1:] if search else ""


# MAGIC EXISTS...
# We want to create a search function that handles search terms dynamically.
# We also want to be able to call help(func) and see the fiels in the help call.
# TODO: make help() work
def search(cls):
    def wrapper(func):
        def action_wrapper(*args, **kwargs):
            offset = 0
            search_terms = None
            
            # Both of these are primarily used for LazyLookupList
            if 'offset' in kwargs:
                offset = kwargs['offset']
                del kwargs['offset']
            if 'search' in kwargs:
                search_terms = kwargs['search']
                del kwargs['search']

            # If we got a "search" field, just use that instead of what was provided.
            if not search_terms:
                search_terms = get_search_string(cls._object_attributes, kwargs)
            
            if offset:
                return func(*args, offset=offset, search=search_terms)
            else:
                return func(*args, search=search_terms)
        return action_wrapper
    return wrapper