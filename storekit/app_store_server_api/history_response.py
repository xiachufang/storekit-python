from typing import List, Optional

from pydantic import BaseModel, Field

from storekit.models import Environment, JWSTransactionDecodedPayload


class GetTransactionHistoryQueryParameters(BaseModel):
    revision: Optional[str]
    start_date: Optional[int] = Field(alias="startDate")
    end_date: Optional[int] = Field(alias="endDate")
    product_id: Optional[str] = Field(alias="productId")
    product_type: Optional[str] = Field(
        alias="productType", description="Possible values: AUTO_RENEWABLE, NON_RENEWABLE, CONSUMABLE, NON_CONSUMABLE"
    )
    sort: Optional[str] = Field(description="Possible values: ASCENDING, DESCENDING")
    subscription_group_identifier: Optional[str] = Field(alias="subscriptionGroupIdentifier")
    in_app_ownership_type: Optional[str] = Field(
        alias="inAppOwnershipType", description="Possible values: FAMILY_SHARED, PURCHASED"
    )
    exclude_revoked: Optional[bool] = Field(alias="excludeRevoked")


class HistoryResponse(BaseModel):
    """
    A response that contains the customer’s transaction history for an app.
    https://developer.apple.com/documentation/appstoreserverapi/historyresponse
    """

    app_apple_id: Optional[int] = Field(alias="appAppleId")
    bundle_id: str = Field(alias="bundleId")
    environment: Environment
    has_more: bool = Field(alias="hasMore")
    revision: str
    transactions: List[JWSTransactionDecodedPayload] = Field(alias="signedTransactions")
