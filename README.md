# Lightspeed HQ API Python Library
Gives easy access to the Lightspeed retail point of sale api.

To use create a new object with settings in a dictionary.  Then just specify
the endpoints and paramaters in your request.

For API documentation see: https://developers.lightspeedhq.com/retail/introduction/introduction/

Some examples of uses:

```python
# Create a new dictionary with some settings that we will need.
import lightspeed_api

c = {'account_id': '12345678',
    'client_id': 'developer_client_id',
    'client_secret': 'developer_client_secret',
    'refresh_token': 'special_refresh_token'
}
    
ls = lightspeed_api.Lightspeed(c)

# Get a customer record
ls.get('Customer/1234')

# Delete a customer by id number
ls.delete('Customer/1234')

# Create a new customer
formatted = {'Customer':
                {'firstName': 'Joe',
                 'lastName': 'Smith',
                 'companyRegistrationNumber': '1234',
                 'customerTypeID': 1,
                 'Contact': {
                     'custom': '',
                     'noEmail': 'false',
                     'noPhone': 'false',
                     'noMail': 'false',
                     'Emails': {
                         'ContactEmail': {
                             'address': 'joe.smith@company.com',
                             'useType': 'Primary'
                         }
                     },
                     'Addresses': {
                         'ContactAddress': {
                             'address1': '1212 Street Drive',
                             'address2': '',
                             'city': 'New York',
                             'state': 'New York',
                             'zip': '12345',
                             'country': 'USA',
                             'countryCode': '',
                             'stateCode': ''
                         }
                     }
                 },
                 }
            }
ls.create("Customer", formatted["Customer"])



```