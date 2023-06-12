import pytest

from storekit.app_store_server_api.transaction_info_response import TransactionInfoResponse


@pytest.fixture()
def transaction_info_response(signed_auto_renewable_subscription_transaction):
    return {
        "signedTransactionInfo": signed_auto_renewable_subscription_transaction,
    }


def test_history_response_content(transaction_info_response):
    resp = TransactionInfoResponse.parse_obj(transaction_info_response)
    assert resp.transaction.transaction_id == "220002745628668"
