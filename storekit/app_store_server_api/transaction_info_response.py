from pydantic import BaseModel, Field

from storekit.models import JWSTransactionDecodedPayload


class TransactionInfoResponse(BaseModel):
    transaction: JWSTransactionDecodedPayload = Field(alias="signedTransactionInfo")
