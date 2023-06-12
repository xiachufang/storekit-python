import pytest

from storekit.app_store_server_api.status_response import StatusResponse


@pytest.fixture()
def status_response_content(signed_renewal_info, signed_auto_renewable_subscription_transaction):
    return {
        "data": [
            {
                "subscriptionGroupIdentifier": "20675086",
                "lastTransactions": [
                    {
                        "originalTransactionId": "510001172393674",
                        "status": 1,
                        "signedRenewalInfo": signed_renewal_info,
                        "signedTransactionInfo": signed_auto_renewable_subscription_transaction,
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
