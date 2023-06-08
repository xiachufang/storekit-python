import pytest

from storekit.app_store_server_api.status_response import StatusResponse


@pytest.fixture()
def status_response_content(jws_mocker):
    return {
        "data": [
            {
                "subscriptionGroupIdentifier": "20675086",
                "lastTransactions": [
                    {
                        "originalTransactionId": "510001172393674",
                        "status": 1,
                        "signedRenewalInfo": jws_mocker.encode(
                            {
                                "originalTransactionId": "220002745628668",
                                "autoRenewProductId": "test_product_2",
                                "productId": "test_product_2",
                                "autoRenewStatus": 0,
                                "environment": "Production",
                                "signedDate": 1678343889311,
                                "recentSubscriptionStartDate": 1678269588000,
                            }
                        ),
                        "signedTransactionInfo": jws_mocker.encode(
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
                    }
                ],
            }
        ],
        "environment": "Production",
        "appAppleId": 1234567890,
        "bundleId": "com.abc",
    }


def test_status_response(status_response_content):
    resp = StatusResponse.parse_obj(status_response_content)
    last_transaction = resp.data[0].last_transactions[0]
    assert last_transaction.renewal_info.original_transaction_id == "220002745628668"
    assert last_transaction.transaction_info.original_transaction_id == "220002745628668"
