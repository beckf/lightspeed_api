
import json
from . import BaseAPI
from ..models.sale import Sale, SaleLine
    

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
            return_list.append(self._unwrap_sales_object(SaleLine, obj))
        
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