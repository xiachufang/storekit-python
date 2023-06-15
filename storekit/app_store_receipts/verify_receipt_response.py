from typing import List, Optional

from pydantic import BaseModel

from storekit.models import AutoRenewStatus, Environment, InAppOwnershipType, PriceIncreaseStatus


class Transaction(BaseModel):
    """
    An in-app purchase transaction.
    https://developer.apple.com/documentation/appstorereceipts/responsebody/latest_receipt_info
    """

    transaction_id: str
    original_transaction_id: str
    product_id: str
    purchase_date: str
    purchase_date_ms: int
    purchase_date_pst: str
    original_purchase_date: str
    original_purchase_date_ms: int
    original_purchase_date_pst: str
    quantity: str
    in_app_ownership_type: InAppOwnershipType
    # only for auto-renewable subscriptions
    web_order_line_item_id: Optional[str] = None
    subscription_group_identifier: Optional[str] = None
    expires_date: Optional[str] = None
    expires_date_ms: Optional[int] = None
    expires_date_pst: Optional[str] = None
    # other scene
    app_account_token: Optional[str] = None
    is_upgraded: Optional[bool] = None
    cancellation_date: Optional[str] = None
    cancellation_date_ms: Optional[int] = None
    cancellation_date_pst: Optional[str] = None
    cancellation_reason: Optional[int] = None
    # offer
    is_in_intro_offer_period: Optional[bool] = None
    is_trial_period: Optional[bool] = None
    offer_code_ref_name: Optional[str] = None
    promotional_offer_id: Optional[str] = None


class Receipt(BaseModel):
    """
    The decoded version of the encoded receipt data that you send with the request to the App Store.
    https://developer.apple.com/documentation/appstorereceipts/responsebody/receipt
    """

    adam_id: int = 0
    app_item_id: int = 0
    application_version: str = ""
    bundle_id: str = ""
    download_id: Optional[int] = None
    expiration_date: str = ""
    expiration_date_ms: int = 0
    expiration_date_pst: str = ""
    in_app: List[Transaction] = []
    original_application_version: str = ""
    original_purchase_date: str = ""
    original_purchase_date_ms: int = 0
    original_purchase_date_pst: str = ""
    preorder_date: str = ""
    preorder_date_ms: int = 0
    preorder_date_pst: str = ""
    receipt_creation_date: str = ""
    receipt_creation_date_ms: int = 0
    receipt_creation_date_pst: str = ""
    receipt_type: str = ""
    request_date: str = ""
    request_date_ms: int = 0
    request_date_pst: str = ""
    version_external_identifier: int = 0


class RenewalInfo(BaseModel):
    """
     An open or failed auto-renewable subscription renewal
    https://developer.apple.com/documentation/appstorereceipts/responsebody/pending_renewal_info
    """

    original_transaction_id: str
    auto_renew_product_id: str
    product_id: str
    auto_renew_status: AutoRenewStatus
    expiration_intent: Optional[int] = None
    grace_period_expires_date: Optional[str] = None
    grace_period_expires_date_ms: Optional[int] = None
    grace_period_expires_date_pst: Optional[str] = None
    is_in_billing_retry_period: Optional[bool] = None
    offer_code_ref_name: Optional[str] = None
    promotional_offer_id: Optional[str] = None
    price_consent_status: Optional[int] = None
    price_increase_status: Optional[PriceIncreaseStatus] = None


class ResponseBody(BaseModel):
    """
    https://developer.apple.com/documentation/appstorereceipts/responsebody
    """

    environment: Environment
    is_retryable: bool = False
    receipt: Receipt
    status: int
    # only for auto-renewable subscriptions
    latest_receipt: str = ""
    latest_receipt_info: List[Transaction] = []
    pending_renewal_info: List[RenewalInfo] = []

    def get_last_transaction(self, product_id: str) -> Optional[Transaction]:
        transactions = [_t for _t in self.latest_receipt_info if _t.product_id == product_id] or [
            _t for _t in self.receipt.in_app if _t.product_id == product_id
        ]

        try:
            return sorted(transactions, key=lambda x: x.purchase_date_ms, reverse=True)[0]
        except IndexError:
            return None

    def get_renewal_info(self, original_transaction_id: str) -> Optional[RenewalInfo]:
        try:
            return next(_r for _r in self.pending_renewal_info if _r.original_transaction_id == original_transaction_id)
        except StopIteration:
            return None
