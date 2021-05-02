
from lightspeed_api.api.queries import _lessthan, _greaterthan, _between, _in, _like, _notequal, _or


def test_search_basic(ls_client):
    _first_name = "Richard"

    customer_list = ls_client.api.customers.all(first_name=_first_name)
    assert(len(customer_list) == 2)
    for c in customer_list:
        assert(c.first_name == _first_name)


def test_search_single_integer(ls_client):
    customer_list = ls_client.api.customers.all(id=1)
    assert(len(customer_list) == 1)
    assert(customer_list[0].id == 1)


def test_or_search(ls_client):
    customer_list = ls_client.api.customers.all(id=_or(1,2))
    assert(len(customer_list) == 2)
    assert(customer_list[0].id == 1)
    assert(customer_list[1].id == 2)