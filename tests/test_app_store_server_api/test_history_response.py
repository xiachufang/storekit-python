import pytest

from storekit.app_store_server_api.history_response import HistoryResponse


@pytest.fixture()
def history_response_content(jws_mocker):
    return {
        "appAppleId": 1234567890,
        "bundleId": "com.abc",
        "environment": "Production",
        "hasMore": False,
        "revision": "1666663790000_1500013720000",
        "signedTransactions": [
            jws_mocker.encode(
                {
                    "transactionId": "300002749490668",
                    "originalTransactionId": "300002749490668",
                    "bundleId": "com.abc",
                    "productId": "test_product_1",
                    "purchaseDate": 1681660134000,
                    "originalPurchaseDate": 1681660134000,
                    "quantity": 1,
                    "type": "Non-Renewing Subscription",
                    "inAppOwnershipType": "PURCHASED",
                    "signedDate": 1681674545204,
                    "environment": "Production",
                }
            ),
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
                    "offerType": 1,
                }
            ),
        ],
    }


def test_history_response_content(history_response_content):
    resp = HistoryResponse.parse_obj(history_response_content)
    assert resp.transactions[0].transaction_id == "300002749490668"
    assert resp.transactions[1].transaction_id == "220002745628668"
