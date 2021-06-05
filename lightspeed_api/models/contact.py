
from datetime import datetime
from . import BaseObject


class Contact(BaseObject):
    _object_attributes = {
        "is_email_allowed": {"type": bool, "ls_field": "noEmail"},
        "is_phone_allowed": {"type": bool, "ls_field": "noPhone"},
        "is_mail_allowed": {"type": bool, "ls_field": "noMail"},
        "last_modified_time": {"type": datetime, "ls_field": "timeStamp"},
        "emails": {"type": 'CustomerEmail', "multifield": True, "ls_field": "Emails.ContactEmail"},
        "phone_numbers": {"type": 'CustomerPhoneNumber', "multifield": True, "ls_field": "Phones.ContactPhone"},
        "addresses": {"type": 'CustomerAddress', "multifield": True, "ls_field": "Addresses.ContactAddress"},
        "website": {"type": str, "ls_field": "Websites.ContactWebsite", "ls_secondary_field": "url", "optional": True},
    }
