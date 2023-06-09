import logging
from typing import Optional

from pydantic import BaseModel, Field

from storekit.jws import JWS
from storekit.models import Environment, JWSRenewalInfoDecodedPayload, JWSTransactionDecodedPayload
from storekit.utils.enum import StrEnum


class NotificationType(StrEnum):
    """
    The type that describes the in-app purchase event for which the App Store sends the version 2 notification.
    https://developer.apple.com/documentation/appstoreservernotifications/notificationtype
    """

    ConsumptionRequest = "CONSUMPTION_REQUEST"
    DidChangeRenewalPref = "DID_CHANGE_RENEWAL_PREF"
    DidChangeRenewalStatus = "DID_CHANGE_RENEWAL_STATUS"
    DidFailToRenew = "DID_FAIL_TO_RENEW"
    DidRenew = "DID_RENEW"
    Expired = "EXPIRED"
    GracePeriodExpired = "GRACE_PERIOD_EXPIRED"
    OfferRedeemed = "OFFER_REDEEMED"
    PriceIncrease = "PRICE_INCREASE"
    Refund = "REFUND"
    RefundDeclined = "REFUND_DECLINED"
    RenewalExtended = "RENEWAL_EXTENDED"
    RenewalExtension = "RENEWAL_EXTENSION"
    Revoke = "REVOKE"
    Subscribed = "SUBSCRIBED"
    Test = "TEST"

    Unknown = "UNKNOWN"

    @classmethod
    def _missing_(cls, value: object) -> "NotificationType":
        logging.error(f"{cls.__name__} Undefined enumeration type: {value}")
        return cls.Unknown


class Subtype(StrEnum):
    """
    A string that provides details about select notification types in version 2.
    https://developer.apple.com/documentation/appstoreservernotifications/subtype
    """

    Accepted = "ACCEPTED"
    AutoRenewDisabled = "AUTO_RENEW_DISABLED"
    AutoRenewEnabled = "AUTO_RENEW_ENABLED"
    BillingRecovery = "BILLING_RECOVERY"
    BillingRetry = "BILLING_RETRY"
    Downgrade = "DOWNGRADE"
    Failure = "FAILURE"
    GracePeriod = "GRACE_PERIOD"
    InitialBuy = "INITIAL_BUY"
    Pending = "PENDING"
    PriceIncrease = "PRICE_INCREASE"
    ProductNotForSale = "PRODUCT_NOT_FOR_SALE"
    Resubscribe = "RESUBSCRIBE"
    Summary = "SUMMARY"
    Upgrade = "UPGRADE"
    Voluntary = "VOLUNTARY"

    Unknown = "UNKNOWN"

    @classmethod
    def _missing_(cls, value: object) -> "Subtype":
        logging.error(f"{cls.__name__} Undefined enumeration type: {value}")
        return cls.Unknown


class Data(BaseModel):
    """
    The app metadata and the signed renewal and transaction information.
    https://developer.apple.com/documentation/appstoreservernotifications/data
    """

    app_apple_id: Optional[int] = Field(None, alias="appAppleId")
    bundle_id: str = Field(alias="bundleId")
    bundle_version: Optional[str] = Field(None, alias="bundleVersion")
    environment: Environment
    renewal_info: Optional[JWSRenewalInfoDecodedPayload] = Field(None, alias="signedRenewalInfo")
    transaction_info: Optional[JWSTransactionDecodedPayload] = Field(None, alias="signedTransactionInfo")


class Summary(BaseModel):
    """
    The payload data for a subscription-renewal-date extension notification.
    https://developer.apple.com/documentation/appstoreservernotifications/summary
    """

    request_identifier: str = Field(alias="requestIdentifier")
    environment: Environment
    app_apple_id: Optional[int] = Field(None, alias="appAppleId")
    bundle_id: str = Field(alias="bundleId")
    product_id: str = Field(alias="productId")
    storefront_country_codes: str = Field(alias="storefrontCountryCodes")
    failed_count: int = Field(alias="failedCount")
    succeeded_count: int = Field(alias="succeededCount")


class ResponseBodyV2DecodedPayload(JWS):
    """A decoded payload containing the version 2 notification data.
    https://developer.apple.com/documentation/appstoreservernotifications/responsebodyv2decodedpayload

    The decoded payload contains the information about the notification.
    Use the notificationType and subtype to understand the event that led to this notification.
    The data object contains the details including the environment,
    the app metadata, and the signed transaction and subscription renewal information.

    The summary object contains information only when the notification is a RENEWAL_EXTENSION with a SUMMARY subtype.
    For more information, see Extend Subscription Renewal Dates for All Active Subscribers.
    """

    notification_type: NotificationType = Field(alias="notificationType")
    subtype: Optional[Subtype] = None
    data: Optional[Data] = Field(
        None,
        description="The data and summary fields are mutually exclusive. The payload contains one of the fields, but not both.",
    )
    summary: Optional[Summary] = Field(
        None,
        description="The data and summary fields are mutually exclusive. The payload contains one of the fields, but not both.",
    )
    version: str
    signed_date: int = Field(alias="signedDate", description="UNIX time, in milliseconds")
    notification_uuid: str = Field(alias="notificationUUID")


class ResponseBodyV2(BaseModel):
    """
    The response body the App Store sends in a version 2 server notification.
    https://developer.apple.com/documentation/appstoreservernotifications/responsebodyv2
    """

    payload: ResponseBodyV2DecodedPayload = Field(alias="signedPayload")
