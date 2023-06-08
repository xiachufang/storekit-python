import pytest

from storekit.app_store_server_api.order_look_up_response import OrderLookupResponse


@pytest.fixture()
def order_look_up_response_content(jws_mocker):
    return {
        "status": 0,
        "signedTransactions": [
            jws_mocker.encode(
                {
                    "transactionId": "220002745628668",
                    "originalTransactionId": "220002745628668",
                    "bundleId": "com.abc",
                    "productId": "test_product_2",
                    "purchaseDate": 1658029753000,
                    "originalPurchaseDate": 1658029755000,
                    "quantity": 1,
                    "type": "Auto-Renewable Subscription",
                    "inAppOwnershipType": "PURCHASED",
                    "signedDate": 1681674933496,
                    "environment": "Production",
                    "webOrderLineItemId": "220001229462830",
                    "subscriptionGroupIdentifier": "41350172",
                    "expiresDate": 1660708153000,
                }
            ),
        ]
        * 3,
    }


def test_order_look_up_response(order_look_up_response_content):
    resp = OrderLookupResponse.parse_obj(order_look_up_response_content)
    transaction = resp.transactions[0]
    assert transaction.transaction_id == "220002745628668"
