
from urllib.parse import quote_plus

def _lessthan(value, or_equal=False):
    # TODO: do we need to check this is an int, or does it work on strings?
    # TODO: do we need to check this is a datetime/float as well? 
    def evaluate_query(field):
        return f"{field}=<{'%3D' if or_equal else ''},{value}"
    return evaluate_query

def _greaterthan(value, or_equal=False):
    # TODO: do we need to check this is an int, or does it work on strings?
    # TODO: do we need to check this is a datetime/float as well? 
    def evaluate_query(field):
        return f"{field}=>{'%3D' if or_equal else ''},{value}"
    return evaluate_query

def _between(lesser_value, greater_value):
    def evaluate_query(field):
        try:
            # Testing these values
            # TODO: do we need to check this is a datetime/float as well? 
            int(lesser_value)
            int(greater_value)
            return f"{field}=><,{lesser_value},{greater_value}"
        except ValueError:
            raise Exception("_between operator cannot be used on non-integer values: "
                "'%s' and '%s' were provided" % (lesser_value, greater_value))
    return evaluate_query

def _notequal(value):
    def evaluate_query(field):
        return f"{field}=!%3D,{quote_plus(value)}"
    return evaluate_query

# TODO: handle wildcards "*" to be "%" instead?
# TODO: should we confirm we don't handle ints here?
def _like(value, notlike=False):
    def evaluate_query(field):
        return f"{field}={'!' if notlike else ''}~,{quote_plus(value)}"
    return evaluate_query

# TODO: can this handle string values?
def _in(*values):
    def evaluate_query(field):
        search = ""
        for v in values:
            try:
                # Testing this value
                int(v)
                search += f",{v}"
            except ValueError:
                raise Exception("_in operator cannot be used on non-integer values: '%s' was provided" % v)
        return f"{field}=IN,[{search[1:] if search else ''}]"
    return evaluate_query


def _or(*statements):
    def evaluate_query(field):
        search = ""
        for s in statements:
            if callable(s):
                evaluated = s(field)
                if evaluated.startswith("or="):
                    # This means we're trying to embed an _or inside an _or
                    # This won't work with LightSpeed's API
                    raise Exception("_or query inside an _or query will not work - error!")
                elif "&" in evaluated:
                    # This means we're trying to embed an _and inside an _or
                    # This won't work with LightSpeed's API
                    raise Exception("_and query inside an _or query will not work - error!")
                search += f"|{quote_plus(evaluated)}"
            else:
                evaluated = quote_plus(f"{field}={quote_plus(s)}")
                search += f"|{evaluated}"
        return f"or={search[1:] if search else ''}"
    return evaluate_query