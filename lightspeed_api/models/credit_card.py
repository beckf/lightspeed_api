
from datetime import datetime
from . import BaseObject


class CreditCardCharge(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "ccChargeID"},
        "transaction_id": {"type": str, "ls_field": "gatewayTransID"},
        "card_last_4_digits": {"type": str, "ls_field": "xnum"},
        "response": {"type": str, "ls_field": "response"},
        "is_voided": {"type": bool, "ls_field": "voided"},
        "refunded_amount": {"type": float, "ls_field": "refunded"},
        "charged_amount": {"type": float, "ls_field": "amount"},
        "card_expiry": {"type": str, "ls_field": "exp"},
        "is_auth_only": {"type": bool, "ls_field": "authOnly"},
        "authorization_code": {"type": str, "ls_field": "authCode"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "is_declined": {"type": bool, "ls_field": "declined"},
        "entry_method": {"type": str, "ls_field": "entryMethod"},
        "cardholder_name": {"type": str, "ls_field": "cardholderName"},
        "communication_key": {"type": str, "ls_field": "communicationKey"},
        "sale": {"type": 'Sale', "ls_field_id": "saleID"},
        "payments": {"type": 'SalePayment', "multifield": True, "ls_field": "SalePayments", "relationships": ["SalePayments"]},
    }


class CreditCardGateway(BaseObject):
    _object_attributes = {
        "id": {"type": int, "ls_field": "ccGatewayID"},
        "login": {"type": str, "ls_field": "login"},
        "market_type": {"type": str, "ls_field": "marketType"},
        "transaction_key": {"type": str, "ls_field": "transKey"},
        "device_type": {"type": int, "ls_field": "deviceType"},
        "hash": {"type": str, "ls_field": "hashValue"},
        "is_enabled": {"type": bool, "ls_field": "enabled"},
        "is_test_mode_enabled": {"type": bool, "ls_field": "testMode"},
        "gateway_name": {"type": str, "ls_field": "gateway"},
        "account_number": {"type": str, "ls_field": "accountNum"},
        "terminal_id": {"type": str, "ls_field": "terminalNum"},
        "is_credit_card_charges_allowed": {"type": bool, "ls_field": "allowCredits"},
        "other_credentials_1": {"type": str, "ls_field": "otherCredentials1"},
        "other_credentials_2": {"type": str, "ls_field": "otherCredentials2"},
        "visa_payment_type": {"type": 'PaymentType', "ls_field_id": "visaPaymentTypeID"},
        "mastercard_payment_type": {"type": 'PaymentType', "ls_field_id": "masterPaymentTypeID"},
        "discover_payment_type": {"type": 'PaymentType', "ls_field_id": "discoverPaymentTypeID"},
        "debit_payment_type": {"type": 'PaymentType', "ls_field_id": "debitPaymentTypeID"},
        "american_payment_type": {"type": 'PaymentType', "ls_field_id": "americanPaymentTypeID"},
    }