
from datetime import datetime

import lightspeed_api


def test_customer_create(ls_client):
    customer = lightspeed_api.models.Customer()
    customer.first_name = "Test"
    ls_client.api.add(customer)
    customer.save()
    assert(customer.id != None)

    id = customer.id
    customer.last_name = "Buddy"
    customer.save()
    assert(customer.id == id)
    assert(customer.first_name == "Test")
    assert(customer.last_name == "Buddy")

    customer.delete()
    customer_list = ls_client.api.customers.all(id=id)
    assert(len(customer_list) == 0)


def test_customer_create_invalid(ls_client):
    customer = lightspeed_api.models.Customer()
    ls_client.api.add(customer)
    try:
        customer.save()
        assert(False)
    except lightspeed_api.client.HTTPServerError as ex:
        pass        # Success case


def test_customer_create_complex(ls_client):
    customer = lightspeed_api.models.Customer()
    customer.first_name = "Jimmy"
    customer.last_name = "Bob"
    customer.title = "CFO"
    customer.birthday = datetime.now().date()
    customer.company = "Home Depot"
    customer.type = ls_client.api.customers.get_customer_type(1)

    email1 = lightspeed_api.models.CustomerEmail("tst@hdepot.com", lightspeed_api.models.CustomerEmailType.PRIMARY)
    email2 = lightspeed_api.models.CustomerEmail("someotheremail@fakenews.com", lightspeed_api.models.CustomerEmailType.SECONDARY)
    customer.emails = [email1, email2]

    phone1 = lightspeed_api.models.CustomerPhoneNumber("+16138311828", lightspeed_api.models.CustomerPhoneNumberType.WORK)
    phone2 = lightspeed_api.models.CustomerPhoneNumber("6131234567", lightspeed_api.models.CustomerPhoneNumberType.FAX)
    customer.phone_numbers = [phone1, phone2]

    customer.website = "www.google.com"
    
    address1 = lightspeed_api.models.CustomerAddress()
    address1.address_line_1 = "123 Fake St"
    address1.address_line_2 = "Unit 1"
    address1.city = "Ottawa"
    address1.state = "Ontario"
    address1.country = "Canada"
    address1.zipcode = "A1A 1A1"
    customer.addresses.append(address1)

    t1 = lightspeed_api.models.Tag()
    t1.name = "fullprofile"
    t2 = lightspeed_api.models.Tag()
    t2.name = "testaccount"
    customer.tags = [t1, t2]
    customer.note = lightspeed_api.models.Note()
    customer.note.text = "This is just a test to ensure that notes can be made!"
    
    # TODO: discount
    # TODO: custom fields?

    ls_client.api.add(customer)     # Should create everything!
    customer.save()

    customer_copy = ls_client.api.customers.all(id=customer.id)[0]
    try:
        assert(customer.first_name == customer_copy.first_name)
        assert(customer.last_name == customer_copy.last_name)
        assert(customer_copy.name == "Jimmy Bob")
        assert(customer.title == customer_copy.title)
        # TODO: fix this once UTC is done [TICKET 1]
        #assert(customer.birthday == customer_copy.birthday)
        assert(customer.company == customer_copy.company)
        assert(customer.type == customer_copy.type)
        assert(customer.emails == customer_copy.emails)
        assert(customer.tags == customer_copy.tags)
        assert(customer.note == customer_copy.note)
        assert(customer_copy.note.last_modified_time < datetime.utcnow())
    except AssertionError as ex:
        customer.delete()       # Delete if things failed.
        raise ex
    
    customer.delete()


def test_customer_all_functions(ls_client):
    obj_list = ls_client.api.customers.all()
    assert(len(obj_list) > 0)

    obj_list = ls_client.api.customers.all_customer_types()
    assert(len(obj_list) > 0)

    obj_list = ls_client.api.customers.all_customer_custom_fields()
    assert(len(obj_list) > 0)


def test_customer_get_functions(ls_client):
    obj = ls_client.api.customers.get_customer(1)
    assert(obj is not None)

    obj = ls_client.api.customers.get_customer_type(1)
    assert(obj is not None)

    obj = ls_client.api.customers.get_customer_custom_field(1)
    assert(obj is not None)


def test_customer_anonymize_delete(ls_client):
    # TODO: write test
    assert(False)


def test_customer_create_all_fields_and_anonymize(ls_client):
    # TODO: write test
    assert(False)


def test_customer_create_all_fields(ls_client):
    # TODO: write test
    assert(False)


def test_customer_get_created_from_ls(ls_client):
    customer = ls_client.api.customers.get_customer(2)
    assert(customer is not None)
    assert(customer.type is not None)
    assert(customer.type.id == 1)
    
    assert(len(customer.emails) == 2)
    for t in customer.emails:
        assert(t is not None)
        assert(t.address is not None)
        assert(t.type == lightspeed_api.models.CustomerEmailType.PRIMARY or
                t.type == lightspeed_api.models.CustomerEmailType.SECONDARY)
    
    assert(len(customer.phone_numbers) == 5)
    for t in customer.phone_numbers:
        assert(t is not None)
        assert(t.number is not None)
        if t.number == "1111111111":
            assert(t.type == lightspeed_api.models.CustomerPhoneNumberType.HOME)
        elif t.number == "2222222222":
            assert(t.type == lightspeed_api.models.CustomerPhoneNumberType.WORK)
        elif t.number == "4444444444":
            assert(t.type == lightspeed_api.models.CustomerPhoneNumberType.PAGER)
        elif t.number == "3333333333":
            assert(t.type == lightspeed_api.models.CustomerPhoneNumberType.MOBILE)
        elif t.number == "5555555555":
            assert(t.type == lightspeed_api.models.CustomerPhoneNumberType.FAX)
        else:
            assert(False)

    assert(len(customer.addresses) == 1)
    for t in customer.addresses:
        assert(t is not None)
        assert(t.address_line_1 == "1 Wellington St")
        assert(t.address_line_2 == "ATTN: Someone")
        assert(t.city == "Ottawa")
        assert(t.state == "Ontario")
        assert(t.zipcode == "K1A 0A6")
        assert(t.country == "Canada")

    assert(len(customer.tags) > 0)
    for t in customer.tags:
        assert(t.id)

    assert(customer.website == "www.canada.ca")
    assert(customer.credit_account is not None)
    assert(customer.discount is not None)
    assert(customer.discount.id == 1)
    assert(customer.tax_category is not None)
    assert(customer.tax_category.id == 1)
    assert(customer.note is not None)
    assert(customer.note.text == "Testing 123")
    assert(customer.note.is_public == False)
    assert(customer.note.last_modified_time < datetime.utcnow())

    assert(len(customer.custom_fields) > 0)
    for c in customer.custom_fields:
        assert(c.id)
        if c.id == 2:
            assert(c.value == '100')
            assert(c.custom_field.id == 1)
            assert(c.custom_field.name == c.name)
            assert(c.custom_field.type == c.type)
            assert(c.custom_field.units == "thx")

    assert(customer.birthday is not None and customer.birthday < datetime.utcnow().date())
    assert(customer.created_time is not None and customer.created_time < datetime.utcnow())
    assert(customer.last_modified_time is not None and customer.last_modified_time < datetime.utcnow())
    assert(customer.title == "CTO")
    assert(customer.first_name == "Richard")
    assert(customer.last_name == "Desmarais")
    assert(customer.name == "Richard Desmarais")
    assert(customer.company == "Dayna's Pet Sitting")


def test_customer_check_types_from_ls(ls_client):
    # TODO: write test
    assert(False)


def test_customer_full_load_no_network_afterwards(ls_client):
    # TODO: write test
    # TODO: nop out the API object in the customer after loading it
    assert(False)


def test_customer_unknown(ls_client):
    # TODO: write test (and determine what it is for)
    assert(False)


def test_customer_print_items(ls_client):
    # TODO: write test
    # Meant to test that printing the fields of this object actually works and throws no errors.
    assert(False)