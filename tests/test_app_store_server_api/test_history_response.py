import pytest

from storekit.app_store_server_api.history_response import HistoryResponse


@pytest.fixture()
def history_response_content(
    signed_non_renewing_subscription_transaction, signed_auto_renewable_subscription_transaction
):
    return {
        "appAppleId": 1234567890,
        "bundleId": "com.abc",
        "environment": "Production",
        "hasMore": False,
        "revision": "1666663790000_1500013720000",
        "signedTransactions": [
            signed_non_renewing_subscription_transaction,
            signed_auto_renewable_subscription_transaction,
        ],
    }


def test_history_response_content(history_response_content):
    resp = HistoryResponse.parse_obj(history_response_content)
    assert resp.transactions[0].transaction_id == "300002749490668"
    assert resp.transactions[1].transaction_id == "220002745628668"
