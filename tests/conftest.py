
import os
import pytest

import lightspeed_api

LIGHTSPEED_CLIENT_ID = os.environ.get('LIGHTSPEED_CLIENT_ID')
LIGHTSPEED_SECRET_ID = os.environ.get('LIGHTSPEED_SECRET_ID')
LIGHTSPEED_REFRESH_TOKEN = os.environ.get('LIGHTSPEED_REFRESH_TOKEN')

LIGHTSPEED_INSTANCE = None


@pytest.fixture
def ls_client():
    global LIGHTSPEED_INSTANCE
    if not LIGHTSPEED_INSTANCE:
        client_payload = {
            'client_id': LIGHTSPEED_CLIENT_ID,
            'client_secret': LIGHTSPEED_SECRET_ID,
            'refresh_token': LIGHTSPEED_REFRESH_TOKEN
        }
        LIGHTSPEED_INSTANCE = lightspeed_api.Lightspeed(client_payload)
    return LIGHTSPEED_INSTANCE