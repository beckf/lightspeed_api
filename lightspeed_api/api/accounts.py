
from . import BaseAPI


class AccountsAPI(BaseAPI):
    def get_account_id(self):
        data = self.client.request(
            'GET',
            'https://api.lightspeedapp.com/API/Account.json'
        )   
        return data['Account']['accountID']