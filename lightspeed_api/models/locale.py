
from . import BaseObject

class CurrencyDenomination(BaseObject):
    _object_attributes = {
        "name": {"type": str, "ls_field": "name"},
        "value": {"type": str, "ls_field": "value"},
        "is_significant": {"type": bool, "ls_field": "significant"},
    }


class Locale(BaseObject):
    _object_attributes = {
        "name": {"type": str, "ls_field": "name"},
        "country": {"type": str, "ls_field": "country"},
        "states": {"type": str, "ls_field": "states"},  # TODO: formatting of this magically? from list to concat'd string?
        "currency_symbol": {"type": str, "ls_field": "currencySymbol"},
        "currency_code": {"type": str, "ls_field": "currencyCode"},
        "currency_precision": {"type": float, "ls_field": "currencyPrecision"},
        "cash_rounding_precision": {"type": float, "ls_field": "cashRoundingPrecision"},
        "is_include_tax_on_labels": {"type": bool, "ls_field": "includeTaxOnLabels"},
        "language_tag": {"type": str, "ls_field": "languageTag"},
        "date_format": {"type": str, "ls_field": "dateFormat"},
        "datetime_format": {"type": str, "ls_field": "dateTimeFormat"},
        "denominations": {"type": 'CurrencyDenomination', "multifield": True, "ls_field": "CurrencyDenominations.CurrencyDenomination"},
        "tax_name_1": {"type": str, "ls_field": "taxName1"},
        "tax_name_2": {"type": str, "ls_field": "taxName2"},
    }