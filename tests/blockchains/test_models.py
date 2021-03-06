import copy

import pytest

from cc_framework.blockchain import connectors, exceptions, models
from tests.blockchains.connectors import data


class TestNode:

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures('bitcoin_core_node')
    def test_process_receipts(monkeypatch):
        monkeypatch.setattr(
            connectors.btc.BitcoinCoreConnector,
            '_request',
            lambda *_: data.BTC_TXS,
        )
        assert models.Node.objects.all().count() == 1
        models.Node.objects.process_receipts()
        txs = models.Transaction.objects.all()
        assert txs.count() == 2
        assert txs.filter(is_confirmed=True).count() == 1

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures('bitcoin_core_node')
    def test_confirm_charged_receipts(monkeypatch):
        # Increases confirmations number for the first tx in test_btc.TXS
        mock_txs = copy.deepcopy(data.BTC_TXS)
        mock_txs[0]['confirmations'] = 666

        monkeypatch.setattr(
            connectors.btc.BitcoinCoreConnector,
            '_request',
            lambda *_: mock_txs,
        )

        models.Node.objects.process_receipts()
        txs = models.Transaction.objects.all()
        assert txs.filter(is_confirmed=True).count() == 2

    @staticmethod
    @pytest.mark.django_db
    def test_node_does_not_exist_error(bitcoin_currency):
        with pytest.raises(exceptions.NodeDoesNotExistError):
            models.Node.objects.create(
                name='bitcoin-lol',
                currency=bitcoin_currency,
                rpc_username='bitcoin',
                rpc_password='qwerty54',
                rpc_host='example.com',
                rpc_port=18332,
            )


class TestCurrency:

    @staticmethod
    def test_create_rises_node_does_not_exist_error():
        with pytest.raises(exceptions.CurrencyDoesNotExistError):
            models.Currency.objects.create(
                name='LOL',
                min_confirmations=2,
            )

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures('bitcoin_core_node')
    def test_default_node(bitcoin_currency):
        assert bitcoin_currency.default_node.name == 'bitcoin-core'

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures('bitcoin_core_node')
    def test_create_two_default_node_raises_error(bitcoin_currency):
        with pytest.raises(exceptions.DefaultNodeAlreadyExists):
            models.Node.objects.create(
                name='bitcoin-core',
                currency=bitcoin_currency,
                is_default=True,
                rpc_username='bitcoin',
                rpc_password='qwerty54',
                rpc_host='example.com',
                rpc_port=18332,
            )

    # TODO: Add default errors test
