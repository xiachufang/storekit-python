import pytest

from storekit.app_store_server_api.order_look_up_response import OrderLookupResponse


@pytest.fixture()
def order_look_up_response_content(signed_auto_renewable_subscription_transaction):
    return {
        "status": 0,
        "signedTransactions": [signed_auto_renewable_subscription_transaction] * 3,
    }


def test_order_look_up_response(order_look_up_response_content):
    resp = OrderLookupResponse.parse_obj(order_look_up_response_content)
    transaction = resp.transactions[0]
    assert transaction.transaction_id == "220002745628668"
