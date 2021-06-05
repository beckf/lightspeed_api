
from datetime import datetime
import lightspeed_api


def test_vendor_create(ls_client):
    vendor = lightspeed_api.models.Vendor()
    vendor.name = "Fake Vendor"
    ls_client.api.add(vendor)
    vendor.save()
    assert(vendor.id != None)

    id = vendor.id
    vendor.account_number = "123456789"
    vendor.save()
    assert(vendor.id == id)
    assert(vendor.name == "Fake Vendor")
    assert(vendor.account_number == "123456789")

    vendor.delete()
    vendor_list = ls_client.api.vendors.all(id=id)
    assert(len(vendor_list) == 0)


def test_vendor_create_invalid(ls_client):
    vendor = lightspeed_api.models.Vendor()
    ls_client.api.add(vendor)
    try:
        vendor.save()
        assert(False)
    except Exception as ex:
        pass        # Success case


def test_vendor_all_functions(ls_client):
    obj_list = ls_client.api.vendors.all()
    assert(len(obj_list) == 9)


def test_vendor_get_functions(ls_client):
    obj = ls_client.api.vendors.get_vendor(1)
    assert(obj is not None)


def test_vendor_get_created_from_ls(ls_client):
    vendor = ls_client.api.vendors.get_vendor(1)
    assert(vendor is not None)

    assert(len(vendor.representatives) == 1)
    for t in vendor.representatives:
        assert(t is not None)
        assert(isinstance(t, lightspeed_api.models.VendorRepresentative))
        assert(t.name=="John Doe")
