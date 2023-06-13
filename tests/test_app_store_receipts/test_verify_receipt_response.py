import pytest

from storekit.app_store_receipts.verify_receipt_response import ResponseBody


@pytest.fixture()
def verify_receipt_response(jws_mocker):
    return {
        "environment": "Production",
        "receipt": {
            "receipt_type": "Production",
            "adam_id": 2754164334,
            "app_item_id": 2754164334,
            "bundle_id": "com.abc",
            "application_version": "164",
            "download_id": 500628332437815653,
            "version_external_identifier": 856208937,
            "receipt_creation_date": "2023-06-09 10:36:51 Etc/GMT",
            "receipt_creation_date_ms": "1686307011000",
            "receipt_creation_date_pst": "2023-06-09 03:36:51 America/Los_Angeles",
            "request_date": "2023-06-09 11:00:19 Etc/GMT",
            "request_date_ms": "1686308419189",
            "request_date_pst": "2023-06-09 04:00:19 America/Los_Angeles",
            "original_purchase_date": "2021-08-15 03:26:57 Etc/GMT",
            "original_purchase_date_ms": "1628998017000",
            "original_purchase_date_pst": "2021-08-14 20:26:57 America/Los_Angeles",
            "original_application_version": "138",
            "in_app": [
                {
                    "quantity": "1",
                    "product_id": "test_product_2",
                    "transaction_id": "225000725999746",
                    "original_transaction_id": "225000725999746",
                    "purchase_date": "2023-06-09 10:36:49 Etc/GMT",
                    "purchase_date_ms": "1686307009000",
                    "purchase_date_pst": "2023-06-09 03:36:49 America/Los_Angeles",
                    "original_purchase_date": "2023-06-09 10:36:51 Etc/GMT",
                    "original_purchase_date_ms": "1686307011000",
                    "original_purchase_date_pst": "2023-06-09 03:36:51 America/Los_Angeles",
                    "expires_date": "2023-07-09 10:36:49 Etc/GMT",
                    "expires_date_ms": "1688899009000",
                    "expires_date_pst": "2023-07-09 03:36:49 America/Los_Angeles",
                    "web_order_line_item_id": "225000335955614",
                    "is_trial_period": "false",
                    "is_in_intro_offer_period": "true",
                    "in_app_ownership_type": "PURCHASED",
                }
            ],
        },
        "latest_receipt_info": [
            {
                "quantity": "1",
                "product_id": "test_product_2",
                "transaction_id": "225000725999746",
                "original_transaction_id": "225000725999746",
                "purchase_date": "2023-06-09 10:36:49 Etc/GMT",
                "purchase_date_ms": "1686307009000",
                "purchase_date_pst": "2023-06-09 03:36:49 America/Los_Angeles",
                "original_purchase_date": "2023-06-09 10:36:51 Etc/GMT",
                "original_purchase_date_ms": "1686307011000",
                "original_purchase_date_pst": "2023-06-09 03:36:51 America/Los_Angeles",
                "expires_date": "2023-07-09 10:36:49 Etc/GMT",
                "expires_date_ms": "1688899009000",
                "expires_date_pst": "2023-07-09 03:36:49 America/Los_Angeles",
                "web_order_line_item_id": "225000335955614",
                "is_trial_period": "false",
                "is_in_intro_offer_period": "true",
                "in_app_ownership_type": "PURCHASED",
                "subscription_group_identifier": "10273352",
            }
        ],
        "latest_receipt": "a base64 string",
        "pending_renewal_info": [
            {
                "auto_renew_product_id": "test_product_2",
                "product_id": "test_product_2",
                "original_transaction_id": "225000725999746",
                "auto_renew_status": "1",
            }
        ],
        "status": 0,
    }


def test_verify_receipt_response(verify_receipt_response):
    resp = ResponseBody.parse_obj(verify_receipt_response)

    last_transaction = resp.get_last_transaction("test_product_2")
    assert last_transaction.transaction_id == "225000725999746"

    renewal_info = resp.get_renewal_info(last_transaction.original_transaction_id)
    assert renewal_info.original_transaction_id == "225000725999746"
