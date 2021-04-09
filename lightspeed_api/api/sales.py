
import json
from . import BaseAPI, BaseObject

class Sale(BaseObject):
    def __init__(self, obj=None, api=None):
        if obj:
            self.id = obj['saleID']
            self.timestamp = obj['timeStamp']
            self.completed = obj['completed']
            self.total = obj['calcTotal']
            self.customer_id = obj['customerID']
            self.internal_note_id = "0" if "SaleNotes" not in obj or "InternalNote" not in obj["SaleNotes"] else obj["SaleNotes"]["InternalNote"]['noteID']
            self.internal_note = "" if self.internal_note_id == "0" else obj["SaleNotes"]["InternalNote"]["note"]
            self.printed_note_id = "0" if "SaleNotes" not in obj or "PrintedNote" not in obj["SaleNotes"] else obj["SaleNotes"]["PrintedNote"]['noteID']
            self.printed_note = "" if self.printed_note_id == "0" else obj["SaleNotes"]["PrintedNote"]['note']
            self._obj = obj
    
    @property
    def items(self):
        return self.api.sales.get_all_from_sale(self.id)
    
    def has_customer(self):
        return self.customer_id != "0"

    @property
    def customer(self):
        if self.customer_id == "0":
            return None
        return self.api.customers.get_customer(self.customer_id)
    
    def set_note(self, note):
        return self.api.sales.set_note(self.id, note)


class SoldItem(BaseObject):
    def __init__(self, obj=None, api=None):
        if obj:
            self.id = obj['saleLineID']
            self.sale_id = obj['saleID']
            self.item_id = obj['itemID']
            self.created_at = obj['createTime']
            self.total = obj['calcTotal']
            self.count = int(obj['unitQuantity'])
            self._obj = obj
    
    @property
    def tags(self):
        return self.api.items.get_tags_for_item(self.item_id)
    
    @property
    def item(self):
        return self.api.items.get_item(self.item_id)

    @property
    # TODO: figure out how to pass in the object (if it existed) instead of re-looking it up.
    def sale(self):
        return self.api.sales.get_sale(self.sale_id)
    
    def set_note(self, note):
        return self.api.sales.set_item_note(self.id, self.sale_id, note)
    

class SalesAPI(BaseAPI):
    def all(self, open=None):
        data = self.client.request('GET', f'Sale.json')
        return_list = self._create_forever_list(data, Sale, self.all)       # TODO: functools partial this.
        return return_list
    
    def get_sale(self, SaleID):
        data = self.client.request('GET', f'Sale/{SaleID}.json?load_relations=["SaleNotes"]')
        if data is None:
            return []
        
        return self._unwrap_sales_object(Sale, data['Sale'])
    
    def get_active_sale_at_register(self, RegisterID):
        data = self.client.request('GET', f'Sale.json?registerID={RegisterID}&completed=false&orderby=timeStamp&orderby_desc=1&limit=1')
        if data is None or 'Sale' not in data:
            return None
        
        return self._unwrap_sales_object(Sale, data['Sale'])

    def get_all_from_sale(self, SaleID):
        data = self.client.request('GET', f'Sale/{SaleID}/SaleLine.json')
        if data is None or 'SaleLine' not in data:
            return []
        
        # If there's only a single item in the return, it comes out
        # as a dict instead of a list. Convert it here.
        if type(data['SaleLine']) == dict:
            data['SaleLine'] = [data['SaleLine']]
        
        return_list = []
        for obj in data['SaleLine']:
            return_list.append(self._unwrap_sales_object(SoldItem, obj))
        
        return return_list
    
    def update_sale_line(self, SaleLine):
        self.client.request(
            'PUT',
            f'SaleLine/{SaleLine["saleLineID"]}.json',
            data=json.dumps(SaleLine)
        )
    
    def update_sale_line(self, SaleLine):
        self.client.request(
            'PUT',
            f'SaleLine/{SaleLine["saleLineID"]}.json',
            data=json.dumps(SaleLine)
        )
    
    def get_sales_for_item(self, ItemID, created_at=None):
        url = f'Sale.json?load_relations=["SaleLines"]&SaleLines.itemID={ItemID}'
        if created_at:
            # TODO: handle taking local timezone to UTC before strftiming it.
            str_time = created_at.strftime("%Y-%m-%dT%H:%M:%S")
            url += f"&createTime=>,{str_time}"
        
        data = self.client.request('GET', url)
        if data is None or data['@attributes']['count'] == '0':
            return []
        
        # If there's only a single item in the return, it comes out
        # as a dict instead of a list. Convert it here.
        if type(data['Sale']) == dict:
            data['Sale'] = [data['Sale']]
        
        return_list = []
        for obj in data['Sale']:
            return_list.append(self._unwrap_sales_object(Sale, obj))
        
        return return_list
    
    def set_note(self, SaleID, Note):
        self.client.request(
            'PUT',
            f'Sale/{SaleID}',
            data=json.dumps({
                "SaleNotes":{
                    "PrintedNote": {
                        "note": f"{Note}"
                    }
                }
            })
        )
    
    def set_item_note(self, SaleItemID, SaleID, Note):
        self.client.request(
            'PUT',
            f'Sale/{SaleID}/SaleLine/{SaleItemID}',
            data=json.dumps({
                "Note":{
                    "note": f"{Note}"
                }
            })
        )