from typing import List, Optional

from pydantic import BaseModel, Field

from storekit.models import Environment, JWSTransactionDecodedPayload


class GetTransactionHistoryQueryParameters(BaseModel):
    revision: Optional[str] = None
    start_date: Optional[int] = Field(None, alias="startDate")
    end_date: Optional[int] = Field(None, alias="endDate")
    product_id: Optional[List[str]] = Field(None, alias="productId")
    product_type: Optional[List[str]] = Field(
        None,
        alias="productType",
        description="Possible values: AUTO_RENEWABLE, NON_RENEWABLE, CONSUMABLE, NON_CONSUMABLE",
    )
    sort: Optional[str] = Field(None, description="Possible values: ASCENDING, DESCENDING")
    subscription_group_identifier: Optional[List[str]] = Field(None, alias="subscriptionGroupIdentifier")
    in_app_ownership_type: Optional[str] = Field(
        None, alias="inAppOwnershipType", description="Possible values: FAMILY_SHARED, PURCHASED"
    )
    revoked: Optional[bool] = Field(None, alias="revoked")


class HistoryResponse(BaseModel):
    """
    A response that contains the customer’s transaction history for an app.
    https://developer.apple.com/documentation/appstoreserverapi/historyresponse
    """

    app_apple_id: Optional[int] = Field(None, alias="appAppleId")
    bundle_id: str = Field(alias="bundleId")
    environment: Environment
    has_more: bool = Field(alias="hasMore")
    revision: str
    transactions: List[JWSTransactionDecodedPayload] = Field(alias="signedTransactions")
