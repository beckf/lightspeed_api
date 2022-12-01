import requests
import datetime
import json
import time
from urllib import parse

__author__ = "Forrest Beck"


class Lightspeed(object):

    def __init__(self, config):
        """
        Creates new Lightspeed object.
        :param config: Specify dictionary with config
        """
        self.config = config

        self.token_url = "https://cloud.lightspeedapp.com/oauth/access_token.php"
        if "account_id" in config:
            self.api_url = "https://api.lightspeedapp.com/API/V3/Account/" + config["account_id"] + "/"
        else:
            self.api_url = ""
        # Initialize token as expired.
        self.token_expire_time = datetime.datetime.now() - datetime.timedelta(days=1)
        self.bearer_token = None
        self.rate_limit_bucket_level = None
        self.rate_limit_bucket_rate = 1
        self.rate_limit_last_request = datetime.datetime.now()

        # Create a new session for API calls. This will hold bearer token.
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})

    def __repr__(self):
        return "Lightspeed API"

    def get_authorization_token(self, code):
        """
        Ensures the Lightspeed HQ Bearer token is current
        :return:
        """
        s = requests.Session()

        try:
            payload = {
                'refresh_token': self.config["refresh_token"],
                'client_secret': self.config["client_secret"],
                'client_id': self.config["client_id"],
                'grant_type': 'authorization_code',
                'code': code
            }
            r = s.post(self.token_url, data=payload)
            json = r.json()

            self.bearer_token = json["access_token"]
            self.session.headers.update({'Authorization': 'Bearer ' + self.bearer_token})

            return json["refresh_token"]
        except:
            return None

    def get_token(self):
        """
        Ensures the Lightspeed HQ Bearer token is current
        :return:
        """
        if datetime.datetime.now() > self.token_expire_time:

            s = requests.Session()

            try:
                payload = {
                    'refresh_token': self.config["refresh_token"],
                    'client_secret': self.config["client_secret"],
                    'client_id': self.config["client_id"],
                    'grant_type': 'refresh_token',
                }
                r = s.post(self.token_url, data=payload)
                json = r.json()
                self.token_expire_time = datetime.datetime.now() + \
                                         datetime.timedelta(seconds=int(json["expires_in"]))
                self.bearer_token = json["access_token"]
                self.session.headers.update({'Authorization': 'Bearer ' + self.bearer_token})

                return self.bearer_token
            except:
                return None
        else:
            return self.bearer_token

    def request_bucket(self, method, url, data=None):
        """
        Sends request to session.  Ensures the request doesn't exceed the rate limits of the leaky bucket.
        :param method: post, get, put, delete
        :param url: complete api url
        :param data: post/put data
        :return: results in json
        """

        if self.rate_limit_bucket_level is not None:
            units_available = float(self.rate_limit_bucket_level.split("/")[1]) - float(self.rate_limit_bucket_level.split("/")[0])
        else:
            units_available = 180

        if method in ("post", "put", "delete"):
            units_needed = 10
        else:
            units_needed = 1

        if not units_available >= units_needed:
                left_over = units_needed - units_available
                seconds_wait = left_over / self.rate_limit_bucket_rate
                last_request = datetime.timedelta.total_seconds(datetime.datetime.now() - self.rate_limit_last_request)
                if last_request < seconds_wait:
                    time.sleep(seconds_wait - last_request)

        try:
            tries = 0
            while tries <= 3:
                if method is "post":
                    s = self.session.post(url, data=data)
                elif method is "put":
                    s = self.session.put(url, data=data)
                elif method is "delete":
                    s = self.session.delete(url)
                elif method is "get":
                    s = self.session.get(url)
                # Watch for too many requests status
                if s.status_code == 429:
                    time.sleep(1)
                    tries += 1
                else:
                    break

            if s.status_code == 200:
                # Update time with latest request.
                self.rate_limit_last_request = datetime.datetime.now()
                # Update Bucket Levels
                self.rate_limit_bucket_level = s.headers['X-LS-API-Bucket-Level']
                # Update Drip Rates
                self.rate_limit_bucket_rate = int(s.headers['X-LS-API-Drip-Rate'])

                return s.json()
            else:
                return None

        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)

    def get(self, source, parameters=None):
        """
        Get data from API. Implement pagination.
        :param source: API Source desired
        :param parameters: Optional URL Parameters.
        :return: JSON Results
        """

        # Check the bearer token is up to date.
        self.get_token()

        if parameters:
            url = self.api_url + source + ".json?" + parse.urlencode(parameters, safe=':-')
        else:
            url = self.api_url + source + ".json"

        r = self.request_bucket("get", url)

        if r:
            if r['@attributes']['next']:
                next_page = r['@attributes']['next']
                while True:
                    p = self.request_bucket("get", next_page)
                    next_page = p['@attributes']['next']
                    # Append new data to original request
                    for i in p:
                        if type(p[i]) == list:
                            r[i].extend(p[i])

                    if not next_page:
                        break
        return r

    def create(self, source, data, parameters=None):
        """
        Create new object in API with POST.
        :param source: API Source
        :param data: POST Data
        :param parameters: Optional URL Parameters.
        :return: JSON Results
        """

        # Check the bearer token is up to date.
        self.get_token()

        d = json.dumps(data)

        if parameters:
            url = self.api_url + source + ".json?" + parameters
        else:
            url = self.api_url + source + ".json"

        r = self.request_bucket("post", url, d)
        return r

    def update(self, source, data, parameters=None):
        """
        Update object in API using PUT
        :param source: API Source
        :param data: PUT Data
        :param parameters: Optional URL Parameters.
        :return: JSON Results
        """

        # Check the bearer token is up to date.
        self.get_token()

        d = json.dumps(data)

        if parameters:
            url = self.api_url + source + ".json?" + parameters
        else:
            url = self.api_url + source + ".json"

        r = self.request_bucket("put", url, d)
        return r

    def delete(self, source, parameters=None):
        """
        Delete object from API
        :param source: API Source
        :param parameters: Optional URL Parameters.
        :return: JSON Results
        """

        # Check the bearer token is up to date.
        self.get_token()

        if parameters:
            url = self.api_url + source + ".json?" + parameters
        else:
            url = self.api_url + source + ".json"

        r = self.request_bucket("delete", url)
        return r