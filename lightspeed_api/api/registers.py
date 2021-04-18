
from . import BaseAPI
from ..models.register import Register


class RegistersAPI(BaseAPI):
    def all(self):
        data = self.client.request('GET', f'Register.json')
        if data is None or 'Register' not in data:
            return []
        
        # If there's only a single item in the return, it comes out
        # as a dict instead of a list. Convert it here.
        if type(data['Register']) == dict:
            data['Register'] = [data['Register']]
        
        return_list = self._create_forever_list(data, Register, self.all)       # TODO: functools partial this.
        return return_list