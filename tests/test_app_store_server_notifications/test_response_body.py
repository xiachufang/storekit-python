import pytest

from storekit.app_store_server_notifications.response_body import ResponseBodyV2


@pytest.fixture()
def response_body_content(jws_mocker):
    return {
        "signedPayload": {
            "notificationType": "SUBSCRIBED",
            "subtype": "RESUBSCRIBE",
            "data": {
                "bundleId": "com.abc",
                "bundleVersion": "111",
                "environment": "Production",
                "signedRenewalInfo": jws_mocker.encode(
                    {
                        "originalTransactionId": "220002745628668",
                        "autoRenewProductId": "test_product_2",
                        "productId": "test_product_2",
                        "autoRenewStatus": 1,
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
                    }
                ),
            },
            "version": "2.0",
            "signedDate": 1682028374717,
            "notificationUUID": "09afc32b-747f-47bd-93e2-0f52aca839f7",
        }
    }


def test_status_response(response_body_content):
    body = ResponseBodyV2.parse_obj(response_body_content)
    assert body.payload.notification_type
    assert body.payload.data.transaction_info.transaction_id == "220002745628668"
    assert body.payload.data.renewal_info.original_transaction_id == "220002745628668"
