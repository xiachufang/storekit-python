from storekit.exceptions import StoreKitError


class APIError(StoreKitError):
    def __init__(self, error_code: int, error_message: str):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(self.error_code, self.error_message)


class RetryableError(APIError):
    """
    https://developer.apple.com/documentation/appstoreserverapi/accountnotfoundretryableerror
    """

    _ERROR_CODES = {4040002, 4040004, 4040006, 5000001}

    @classmethod
    def raise_for_api_error(cls, api_error: APIError) -> None:
        if api_error.error_code in cls._ERROR_CODES:
            raise cls(api_error.error_code, api_error.error_message)


class AuthenticationError(StoreKitError):
    """The JSON Web Token (JWT) in the authorization header is invalid. For more information, see Generating Tokens for API Requests.
    https://developer.apple.com/documentation/appstoreserverapi/generating_tokens_for_api_requests
    """

    pass
