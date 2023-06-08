import logging
from typing import List

from pydantic import BaseModel, Field

from storekit.models import JWSTransactionDecodedPayload
from storekit.utils.enum import IntEnum


class OrderLookupStatus(IntEnum):
    """A value that indicates whether the order ID in the request is valid for your app.
    https://developer.apple.com/documentation/appstoreserverapi/orderlookupstatus
    """

    Valid = 0
    Invalid = 1

    Unknown = -1

    @classmethod
    def _missing_(cls, value: object) -> "OrderLookupStatus":
        logging.error(f"{cls.__name__} Undefined enumeration type: {value}")
        return cls.Unknown


class OrderLookupResponse(BaseModel):
    """
    A response that includes the order lookup status and an array of signed transactions for the in-app purchases in the order.
    https://developer.apple.com/documentation/appstoreserverapi/orderlookupresponse
    """

    status: OrderLookupStatus
    transactions: List[JWSTransactionDecodedPayload] = Field(alias="signedTransactions")
