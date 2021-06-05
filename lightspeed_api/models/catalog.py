
from datetime import datetime, date

from . import BaseObject


class CatalogVendor(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "catalogVendorID"},
        "name": {"type": str, "ls_field": "name"},
        "last_updated": {"type": datetime, "ls_field": "lastUpdate"},
    }


class CatalogVendorAvailability(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "catalogVendorID"},
    }


class CatalogVendorItem(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "catalogVendorItemID"},
        "vendor_number": {"type": str, "ls_field": "vendorNumber"},
        "description": {"type": str, "ls_field": "description"},
        "category": {"type": str, "ls_field": "category"},
        "model": {"type": str, "ls_field": "model"},
        "unit_count": {"type": int, "ls_field": "retailUnit"},
        "units": {"type": str, "ls_field": "unitOfMeasurement"},
        "cost": {"type": float, "ls_field": "cost"},
        "cost_discount_1": {"type": float, "ls_field": "costLevel2"},
        "cost_discount_2": {"type": float, "ls_field": "costLevel3"},
        "cost_discount_3": {"type": float, "ls_field": "costLevel4"},
        "msrp": {"type": float, "ls_field": "msrp"},
        "break_count_1": {"type": int, "ls_field": "breakQty"},
        "break_price_1": {"type": float, "ls_field": "breakPrice"},
        "break_count_2": {"type": int, "ls_field": "breakQty2"},
        "break_price_2": {"type": float, "ls_field": "breakPrice2"},
        "break_count_3": {"type": int, "ls_field": "breakQty3"},
        "break_price_3": {"type": float, "ls_field": "breakPrice3"},
        "manufacturer_number": {"type": str, "ls_field": "manufacturerNumber"},
        "brand": {"type": str, "ls_field": "brand"},
        "last_price_change": {"type": date, "ls_field": "lastPriceChange"},
        "upc": {"type": str, "ls_field": "upc"},
        "ean": {"type": str, "ls_field": "ean"},
        "alternate_ean": {"type": str, "ls_field": "ean2"},
        "status": {"type": str, "ls_field": "status"},
        "year": {"type": str, "ls_field": "year"},
        "replacement_item": {"type": str, "ls_field": "replacement"},
        "replacement_description": {"type": str, "ls_field": "replacementDescription"},
        "color": {"type": str, "ls_field": "colorName"},
        "size": {"type": str, "ls_field": "sizeName"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "last_vendor_quantity": {"type": int, "ls_field": "lastQoh"},
        "vendor": {"type": CatalogVendor, "ls_field": "CatalogVendor", "ls_field_id": "catalogVendorID", "relationships": ["CatalogVendor"]},
        "vendor_availability": {"type": CatalogVendorAvailability, "multifield": True, "ls_field": "CatalogVendorAvailability", "relationships": ["CatalogVendor"]},
    }
    _create_url = 'CatalogVendorItem.json'