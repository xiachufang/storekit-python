from storekit.exceptions import StoreKitError


class APIError(StoreKitError):
    """
    https://developer.apple.com/documentation/appstorereceipts/status
    """

    def __init__(self, status: int):
        self.status = status
        super().__init__(self.status)


class RetryableError(APIError):
    """
    An indicator when an error occurs during the request. A value of 1 indicates a temporary issue; retry validation for this receipt at a later time. A value of 0 indicates an unresolvable issue; don’t retry validation for this receipt. This is applicable only to status codes 21100–21199.
    """

    @classmethod
    def raise_for_status(cls, status: int) -> None:
        if status in {21002, 21005, 21009} or 21100 <= status <= 21199:
            raise RetryableError(status)
