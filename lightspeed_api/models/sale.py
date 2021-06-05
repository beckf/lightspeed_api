
from datetime import datetime
from . import BaseObject


class Sale(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "saleID"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "is_completed": {"type": bool, "ls_field": "completed"},
        "is_voided": {"type": bool, "ls_field": "voided"},
        "is_promotions_enabled": {"type": bool, "ls_field": "enablePromotions"},
        "reference_number": {"type": str, "ls_field": "referenceNumber"},
        "reference_number_source": {"type": str, "ls_field": "referenceNumberSource"},
        "tax_rate_1": {"type": float, "ls_field": "tax1Rate"},
        "tax_rate_2": {"type": float, "ls_field": "tax2Rate"},
        "change": {"type": float, "ls_field": "change"},
        "discounted": {"type": float, "ls_field": "calcDiscount"},
        "total_before_discount": {"type": float, "ls_field": "calcTotal"},
        "subtotal": {"type": float, "ls_field": "calcSubtotal"},
        "subtotal_tax": {"type": float, "ls_field": "calcTaxable"},
        "subtotal_nontax": {"type": float, "ls_field": "calcNonTaxable"},
        "average_line": {"type": float, "ls_field": "calcAvgCost"},
        "fifo_cost": {"type": float, "ls_field": "calcFIFOCost"},
        "total_tax_1": {"type": float, "ls_field": "calcTax1"},
        "total_tax_2": {"type": float, "ls_field": "calcTax2"},
        "total_payments": {"type": float, "ls_field": "calcPayments"},
        "total": {"type": float, "ls_field": "total"},
        "due": {"type": float, "ls_field": "totalDue"},
        "displayable_total": {"type": float, "ls_field": "displayableTotal"},
        "balance": {"type": float, "ls_field": "balance"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "updated_time": {"type": datetime, "ls_field": "updateTime"},
        "completed_time": {"type": datetime, "ls_field": "completeTime"},
        "customer": {"type": 'Customer', "ls_field": "Customer", "ls_field_id": "customerID", "relationships": ["Customer"]},
        "employee": {"type": 'Employee', "ls_field_id": "employeeID"},
        "discount": {"type": 'Discount', "ls_field": "Discount", "ls_field_id": "discountID", "relationships": ["Discount"]},
        "tax_category": {"type": 'TaxCategory', "ls_field": "TaxCategory", "ls_field_id": "taxCategoryID", "relationships": ["TaxCategory"]},
        "shop": {"type": 'Shop', "ls_field_id": "shopID"},
        "register": {"type": 'Shop', "ls_field_id": "registerID"},
        "items": {"type": 'SaleLine', "multifield": True, "ls_field": "SaleLines.SaleLine", "relationships": ["SaleLines"]},
        "note": {"type": 'Note', "ls_field": "Note", "relationships": ["SaleNotes"], 'optional': True},
        "payments": {"type": 'SalePayment', "multifield": True, "ls_field": "SalePayments.SalePayment", "relationships": ["SalePayments"]},
        "shipping_info": {"type": 'ShipTo', "ls_field": "ShipTo", "relationships": ["ShipTo"]},
        "quote": {"type": 'Quote', "ls_field": "Quote", "relationships": ["Quote"]},
    }
    _get_function = "SalesAPI.get_sale"
    _update_url = 'Sale/%s.json'
    _create_url = 'Sale.json'

    def email_receipt(self):
        pass

    def refund(self):
        pass


class SaleLine(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "saleLineID"},
        "is_layaway": {"type": bool, "ls_field": "isLayaway"},
        "is_workorder": {"type": bool, "ls_field": "isWorkorder"},
        "is_special_order": {"type": bool, "ls_field": "isSpecialOrder"},
        "is_taxed": {"type": bool, "ls_field": "tax"},
        "quantity": {"type": int, "ls_field": "unitQuantity"},
        "unit_price": {"type": float, "ls_field": "unitPrice"},
        "normal_unit_price": {"type": float, "ls_field": "normalUnitPrice"},
        "discounted": {"type": float, "ls_field": "discountAmount"},
        "discount_percent": {"type": float, "ls_field": "discountPercent"},
        "average_cost": {"type": float, "ls_field": "avgCost"},
        "fifo_cost": {"type": float, "ls_field": "fifoCost"},
        "tax_rate_1": {"type": float, "ls_field": "tax1Rate"},
        "tax_rate_2": {"type": float, "ls_field": "tax2Rate"},
        "displayed_subtotal": {"type": float, "ls_field": "displayableSubtotal"},
        "displayed_unit_price": {"type": float, "ls_field": "displayableUnitPrice"},
        "line_discounted": {"type": float, "ls_field": "calcLineDiscount"},
        "transaction_discounted": {"type": float, "ls_field": "calcTransactionDiscount"},
        "total": {"type": float, "ls_field": "calcTotal"},
        "subtotal": {"type": float, "ls_field": "calcSubtotal"},
        "total_tax_1": {"type": float, "ls_field": "calcTax1"},
        "total_tax_2": {"type": float, "ls_field": "calcTax2"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "discount": {"type": 'Discount', "ls_field": "Discount", "ls_field_id": "discountID", "relationships": ["Discount"]},
        "tax_category": {"type": 'TaxCategory', "ls_field": "TaxCategory", "ls_field_id": "taxCategoryID", "relationships": ["TaxCategory"]},
        "tax_class": {"type": 'TaxClass', "ls_field": "TaxClass", "ls_field_id": "taxClassID", "relationships": ["TaxClass"]},
        "customer": {"type": 'Customer', "ls_field_id": "customerID	"},
        "shop": {"type": 'Shop', "ls_field_id": "shopID"},
        "employee": {"type": 'Employee', "ls_field_id": "employeeID"},
        "register": {"type": 'Shop', "ls_field_id": "registerID"},
        "sale": {"type": 'Sale', "ls_field_id": "saleID"},
        "parent_sale_line": {"type": 'SaleLine', "ls_field_id": "parentSaleLineID"},
        "item": {"type": 'Item', "ls_field": "Item", "ls_field_id": "itemID", "relationships": ["Item"]},
        "note": {"type": 'Note', "ls_field": "Note", "ls_field_id": "noteID", "relationships": ["Note"], 'optional': True},
    }
    
    @property
    def tags(self):
        return self.api.items.get_tags_for_item(self.item_id)
    
    @property
    # TODO: figure out how to pass in the object (if it existed) instead of re-looking it up.
    def sale(self):
        return self.api.sales.get_sale(self.sale_id)
    
    def set_note(self, note):
        return self.api.sales.set_item_note(self.id, self.sale_id, note)


class Quote(BaseObject):
    search_terms = {
        "id": {"type": int, "ls_field": "quoteID"},
        "issue_time": {"type": datetime, "ls_field": "issueDate"},
        "notes": {"type": str, "ls_field": "notes"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "employee": {"type": 'Employee', "ls_field": "employeeID"},
        "sale": {"type": 'Sale', "ls_field": "saleID"},
    }


class SalePayment(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "salePaymentID"},
        "amount": {"type": float, "ls_field": "amount"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "is_archived": {"type": bool, "ls_field": "archived"},
        "client_reference": {"type": str, "ls_field": "remoteReference"},
        "payment_reference": {"type": str, "ls_field": "paymentID"},
        "type": {"type": 'PaymentType', "ls_field": "PaymentType", "ls_field_id": "paymentTypeID", "relationships": ["PaymentType"]},
        "credit_card_charge": {"type": 'CreditCardCharge', "ls_field": "CCCharge", "ls_field_id": "ccChargeID", "relationships": ["CCCharge"]},
        "sale": {"type": 'Sale', "ls_field": "saleID"},
        "referenced_sale_payment": {"type": 'SalePayment', "ls_field": "refPaymentID"},
        "register": {"type": 'Register', "ls_field": "registerID"},
        "credit_account": {"type": 'CreditAccount', "ls_field": "creditAccountID"},
        "employee": {"type": 'Employee', "ls_field": "employeeID"},
        "sale_account": {"type": 'SaleAccount', "ls_field": "SaleAccounts", "relationships": ["SaleAccounts"]},
    }


class SaleAccount(BaseObject):
    _object_attributes = {
        "credit_account": {"type": 'CreditAccount', "ls_field": "creditAccountID"},
        "payment": {"type": 'SalePayment', "ls_field": "salePaymentID"},
        "sale_line": {"type": 'SaleLine', "ls_field": "saleLineID"},
    }


class SalePaymentSignature(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "salePaymentSignatureID"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "payment": {"type": int, "ls_field": "salePaymentID"},
    }


class SaleVoid(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "saleVoidID"},
        "created_time": {"type": datetime, "ls_field": "createTime"},
        "reason": {"type": str, "ls_field": "reason"},
        "sale": {"type": 'Sale', "ls_field": "saleID"},
        "register": {"type": 'Register', "ls_field": "registerID"},
        "employee": {"type": 'Employee', "ls_field": "employeeID"},
    }


class SpecialOrder(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "specialOrderID"},
        "is_customer_contacted": {"type": bool, "ls_field": "contacted"},
        "is_completed": {"type": bool, "ls_field": "completed"},
        "quantity": {"type": int, "ls_field": "unitQuantity"},
        "customer": {"type": 'Customer', "ls_field": "customerID"},
        "shop": {"type": 'Shop', "ls_field": "shopID"},
        "transfer_item": {"type": 'InventoryTransferItem', "ls_field": "transferItemID"},
        "sale_line": {"type": 'SaleLine', "ls_field": "SaleLine", "relationships": ["SaleLine"]},
        "order_line": {"type": 'OrderLine', "ls_field": "OrderLine", "relationships": ["OrderLine"]},
        "note": {"type": 'Note', "ls_field": "Note", "relationships": ["Note"], 'optional': True},
    }