# Lightspeed HQ API Python Library
Based off of https://github.com/beckf/lightspeed_api, this library improves on it and makes it super user-friendly to get complex queries and traversal of Lightspeed items without having to understand the API itself.

For API documentation, see: https://developers.lightspeedhq.com/retail/introduction/introduction/. Note that you can easily see what fields are available/searchable by doing a help() on the function/class you're curious about.

We do a lot of casting/lazy-loading in our system to try and conserve API calls. We've made it possible for you to run your own queries 

Some examples of uses:

```python
# Create a new dictionary with some settings that we will need.
import lightspeed_api

c = {
    'client_id': 'developer_client_id',
    'client_secret': 'developer_client_secret',
    'refresh_token': 'special_refresh_token'
}

ls = lightspeed_api.Lightspeed(c)
client_list = ls.api.customers.all(first_name="Richard")
for client in client_list:          # Infinitely-scrolling lists!
    tag_list = client.tags          # Lazy-loaded attributes as you need them!
    for tag in tag_list:
        items = tag.associated_items        # Extra queries associated to objects!
        for item in items:
            print(item.id, item.sku)

# Do more complex queries
from lightspeed_api.api.queries import _lessthan, _between, _like, _notequal, _or
client_list = ls.api.customers.all(id=_lessthan(300),
                                   last_name=_like("%ich%"),
                                   credit_account_id=_or(_between(0,10), _notequal(40)))

# Create a new item, save it, make a change and then save it again!
from lightspeed_api.api.customers import Customer
cust = Customer()
cust.first_name = "Richard"
cust.last_name = "Desmarais"
cust.save()

print(cust.id)      # Returns a new ID value

cust.credit_account_id = 2
cust.save()

print(cust.id)      # Same ID value as above, object has been updated
```