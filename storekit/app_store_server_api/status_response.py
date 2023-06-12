import logging
from typing import List, Optional

from pydantic import BaseModel, Field

from storekit.models import Environment, JWSRenewalInfoDecodedPayload, JWSTransactionDecodedPayload
from storekit.utils.enum import IntEnum


class GetAllSubscriptionStatusesQueryParameters(BaseModel):
    status: Optional["Status"] = None


class Status(IntEnum):
    """
    The status of an auto-renewable subscription.
    https://developer.apple.com/documentation/appstoreserverapi/status
    """

    Active = 1
    Expired = 2
    InBillingRetryPeriod = 3
    InBillingGracePeriod = 4
    Revoked = 5

    Unknown = -1

    @classmethod
    def _missing_(cls, value: object) -> "Status":
        logging.error(f"{cls.__name__} Undefined enumeration type: {value}")
        return cls.Unknown


class LastTransactionsItem(BaseModel):
    """
    The most recent App Store-signed transaction information and App Store-signed renewal information for an auto-renewable subscription.
    https://developer.apple.com/documentation/appstoreserverapi/lasttransactionsitem
    """

    original_transaction_id: str = Field(alias="originalTransactionId")
    status: Status
    renewal_info: JWSRenewalInfoDecodedPayload = Field(alias="signedRenewalInfo")
    transaction_info: JWSTransactionDecodedPayload = Field(alias="signedTransactionInfo")


class SubscriptionGroupIdentifierItem(BaseModel):
    """
    Information for auto-renewable subscriptions, including signed transaction information and signed renewal information, for one subscription group.
    https://developer.apple.com/documentation/appstoreserverapi/subscriptiongroupidentifieritem
    """

    subscription_group_identifier: str = Field(alias="subscriptionGroupIdentifier")
    last_transactions: List[LastTransactionsItem] = Field(alias="lastTransactions")


class StatusResponse(BaseModel):
    """
    A response that contains status information for all of a customer’s auto-renewable subscriptions in your app.
    https://developer.apple.com/documentation/appstoreserverapi/statusresponse
    """

    data: List[SubscriptionGroupIdentifierItem]
    environment: Environment
    app_apple_id: Optional[int] = Field(None, alias="appAppleId")
    bundle_id: str = Field(alias="bundleId")
