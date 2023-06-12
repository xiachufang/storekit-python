import logging
from typing import Optional

from pydantic import Field

from storekit.jws import JWS
from storekit.utils.enum import IntEnum, StrEnum


class AutoRenewStatus(IntEnum):
    """
    The renewal status for an auto-renewable subscription.
    https://developer.apple.com/documentation/appstoreserverapi/autorenewstatus
    """

    Off = 0
    On = 1

    Unknown = -1

    @classmethod
    def _missing_(cls, value: object) -> "AutoRenewStatus":
        logging.error(f"{cls.__name__} Undefined enumeration type: {value}")
        return cls.Unknown


class Environment(StrEnum):
    Production = "Production"
    Sandbox = "Sandbox"

    Unknown = "UNKNOWN"

    @classmethod
    def _missing_(cls, value: object) -> "Environment":
        logging.error(f"{cls.__name__} Undefined enumeration type: {value}")
        return cls.Unknown


class OfferType(IntEnum):
    """
    The type of subscription offer.
    https://developer.apple.com/documentation/appstoreserverapi/offertype
    """

    IntroductoryOffer = 1
    PromotionalOffer = 2
    SubscriptionOfferCode = 3

    Unknown = -1

    @classmethod
    def _missing_(cls, value: object) -> "OfferType":
        logging.error(f"{cls.__name__} Undefined enumeration type: {value}")
        return cls.Unknown


class PriceIncreaseStatus(IntEnum):
    """
    The status that indicates whether an auto-renewable subscription is subject to a price increase.
    https://developer.apple.com/documentation/appstoreserverapi/priceincreasestatus
    """

    NotResponded = 0
    Consented = 1

    Unknown = -1

    @classmethod
    def _missing_(cls, value: object) -> "PriceIncreaseStatus":
        logging.error(f"{cls.__name__} Undefined enumeration type: {value}")
        return cls.Unknown


class InAppOwnershipType(StrEnum):
    """
    The relationship of the user with the family-shared purchase to which they have access.
    https://developer.apple.com/documentation/appstoreserverapi/inappownershiptype
    """

    FamilyShared = "FAMILY_SHARED"
    Purchased = "PURCHASED"

    Unknown = "UNKNOWN"

    @classmethod
    def _missing_(cls, value: object) -> "InAppOwnershipType":
        logging.error(f"{cls.__name__} Undefined enumeration type: {value}")
        return cls.Unknown


class ProductType(StrEnum):
    """
    The type of in-app purchase products you can offer in your app.
    https://developer.apple.com/documentation/appstoreserverapi/type
    """

    AutoRenewableSubscription = "Auto-Renewable Subscription"
    NonConsumable = "Non-Consumable"
    Consumable = "Consumable"
    NonRenewingSubscription = "Non-Renewing Subscription"

    Unknown = "UNKNOWN"

    @classmethod
    def _missing_(cls, value: object) -> "ProductType":
        logging.error(f"{cls.__name__} Undefined enumeration type: {value}")
        return cls.Unknown


class TransactionReason(StrEnum):
    """
    The cause of a purchase transaction, which indicates whether it’s a customer’s purchase or a renewal for an auto-renewable subscription that the system initiates.
    https://developer.apple.com/documentation/appstoreserverapi/transactionreason
    """

    Purchase = "PURCHASE"
    Renewal = "RENEWAL"

    Unknown = "UNKNOWN"

    @classmethod
    def _missing_(cls, value: object) -> "TransactionReason":
        logging.error(f"{cls.__name__} Undefined enumeration type: {value}")
        return cls.Unknown


class JWSRenewalInfoDecodedPayload(JWS):
    """
    A decoded payload containing subscription renewal information for an auto-renewable subscription.
    https://developer.apple.com/documentation/appstoreserverapi/jwsrenewalinfodecodedpayload
    """

    original_transaction_id: str = Field(alias="originalTransactionId")
    auto_renew_product_id: str = Field(alias="autoRenewProductId")
    product_id: str = Field(alias="productId")
    auto_renew_status: AutoRenewStatus = Field(alias="autoRenewStatus")
    renewal_date: int = Field(alias="renewalDate", description="UNIX time, in milliseconds")
    environment: Environment
    signed_date: int = Field(alias="signedDate", description="UNIX time, in milliseconds")
    recent_subscription_start_date: int = Field(
        alias="recentSubscriptionStartDate", description="UNIX time, in milliseconds"
    )
    expiration_intent: Optional[int] = Field(None, alias="expirationIntent")
    grace_period_expires_date: Optional[int] = Field(
        None, alias="gracePeriodExpiresDate", description="UNIX time, in milliseconds"
    )
    is_in_billing_retry_period: Optional[bool] = Field(None, alias="isInBillingRetryPeriod")
    offer_type: Optional[OfferType] = Field(None, alias="offerType")
    offer_identifier: Optional[str] = Field(None, alias="offerIdentifier")
    price_increase_status: Optional[PriceIncreaseStatus] = Field(None, alias="priceIncreaseStatus")


class JWSTransactionDecodedPayload(JWS):
    """
    A decoded payload containing transaction information.
    https://developer.apple.com/documentation/appstoreserverapi/jwstransactiondecodedpayload
    """

    transaction_id: str = Field(alias="transactionId")
    original_transaction_id: str = Field(alias="originalTransactionId")
    bundle_id: str = Field(alias="bundleId")
    product_id: str = Field(alias="productId")
    purchase_date: int = Field(alias="purchaseDate", description="UNIX time, in milliseconds")
    original_purchase_date: int = Field(alias="originalPurchaseDate", description="UNIX time, in milliseconds")
    quantity: int
    type: ProductType
    in_app_ownership_type: InAppOwnershipType = Field(alias="inAppOwnershipType")
    signed_date: int = Field(alias="signedDate", description="UNIX time, in milliseconds")
    environment: Environment
    storefront: str
    storefront_id: str = Field(alias="storefrontId")
    transaction_reason: TransactionReason = Field(alias="transactionReason")
    # only for auto-renewable subscriptions
    web_order_line_item_id: Optional[str] = Field(None, alias="webOrderLineItemId")
    subscription_group_identifier: Optional[str] = Field(None, alias="subscriptionGroupIdentifier")
    expires_date: Optional[int] = Field(None, alias="expiresDate", description="UNIX time, in milliseconds")
    # other scene
    app_account_token: Optional[str] = Field(None, alias="appAccountToken", description="UUID")
    is_upgraded: Optional[bool] = Field(None, alias="isUpgraded")
    revocation_date: Optional[int] = Field(None, alias="revocationDate", description="UNIX time, in milliseconds")
    revocation_reason: Optional[int] = Field(None, alias="revocationReason")
    # offer
    offer_type: Optional[OfferType] = Field(None, alias="offerType")
    offer_identifier: Optional[str] = Field(None, alias="offerIdentifier")
