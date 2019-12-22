import os

import pytest
from django.conf import settings

from cryptocurrency.blockchains import connectors, models


def pytest_configure():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    settings.configure(
        SECRET_KEY='fake-key',
        INSTALLED_APPS=[
            'tests',
            'cryptocurrency.blockchains',
        ],
        BASE_DIR=base_dir,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(base_dir, 'db.sqlite3'),
            }
        },
    )


@pytest.fixture
def bitcoin_core_connector():
    return connectors.btc.BitcoinCoreConnector(
        rpc_username='bitcoin',
        rpc_password='qwerty54',
        rpc_host='http://example.com',
        rpc_port=18332,
    )


@pytest.fixture
def bitcoin_currency():
    currency = models.Currency.objects.create(name='BTC', min_confirmations=2)
    yield currency
    currency.delete()
