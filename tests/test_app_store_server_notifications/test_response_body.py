import pytest

from storekit.app_store_server_notifications.response_body import ResponseBodyV2


@pytest.fixture()
def response_body_content(signed_renewal_info, signed_auto_renewable_subscription_transaction):
    return {
        "signedPayload": {
            "notificationType": "SUBSCRIBED",
            "subtype": "RESUBSCRIBE",
            "data": {
                "bundleId": "com.abc",
                "bundleVersion": "111",
                "environment": "Production",
                "signedRenewalInfo": signed_renewal_info,
                "signedTransactionInfo": signed_auto_renewable_subscription_transaction,
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
