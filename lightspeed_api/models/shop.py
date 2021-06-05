
from . import BaseObject

class Shop(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "shopID"},
        "name": {"type": str, "ls_field": "name"},
        "labor_rate": {"type": float, "ls_field": "serviceRate"},
        "timezone": {"type": str, "ls_field": "timeZone"},      # TODO: enum?
        "is_labor_taxed": {"type": bool, "ls_field": "taxLabor"},
        "product_title_label": {"type": str, "ls_field": "labelTitle"}, # TODO: ENUM
        "is_msrp_on_label": {"type": bool, "ls_field": "labelMsrp"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "contact": {"type": 'Contact', "ls_field": "Contact", "ls_field_id": "contactID", "relationships": ["Contact"]},        # TODO: implement contact
        "tax_category": {"type": 'TaxCategory', "ls_field": "TaxCategory", "ls_field_id": "taxCategoryID", "relationships": ["TaxCategory"]},
        "receipt_setup": {"type": 'ReceiptSetup', "ls_field": "ReceiptSetup", "ls_field_id": "receiptSetupID", "relationships": ["ReceiptSetup"]},
        "credit_card_gateway": {"type": 'CreditCardGateway', "ls_field": "CCGateway", "ls_field_id": "ccGatewayID", "relationships": ["PriceLevel"]},
        "price_level": {"type": 'PriceLevel', "ls_field": "PriceLevel", "ls_field_id": "priceLevelID", "relationships": ["CCGateway"]},
        "registers": {"type": 'Register', "multifield": True, "ls_field": "Registers.Register", "relationships": ["Registers"]},
    }