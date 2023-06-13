import time
from http import HTTPStatus
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import jwt
import requests

from storekit.utils.enum import StrEnum

from .exceptions import APIError, AuthenticationError, RetryableError
from .history_response import GetTransactionHistoryQueryParameters, HistoryResponse
from .order_look_up_response import OrderLookupResponse
from .status_response import GetAllSubscriptionStatusesQueryParameters, StatusResponse
from .transaction_info_response import TransactionInfoResponse


class BaseUrl(StrEnum):
    Production = "https://api.storekit.itunes.apple.com"
    Sandbox = "https://api.storekit-sandbox.itunes.apple.com"


class SignedTokenEncoder:
    def __init__(self, key_id: str, private_key: str, issuer_id: str, bundle_id: str, algorithm: str = "ES256"):
        self.key_id = key_id
        self.private_key = private_key
        self.issuer_id = issuer_id
        self.bundle_id = bundle_id

        self.algorithm = algorithm

    def __call__(self) -> str:
        jwt_headers = {"alg": self.algorithm, "kid": self.key_id, "typ": "JWT"}
        iat = int(time.time())
        jwt_payload = {
            "iss": self.issuer_id,
            "iat": int(time.time()),
            "exp": iat + 3600,  # 60 minutes timestamp
            "aud": "appstoreconnect-v1",
            "bid": self.bundle_id,
        }
        return jwt.encode(headers=jwt_headers, payload=jwt_payload, key=self.private_key, algorithm=self.algorithm)


class ServerAPIClient:
    def __init__(self, base_url: str, signed_token_encoder: "SignedTokenEncoder", timeout: int = 20):
        self.base_url = base_url
        self.signed_token_encoder = signed_token_encoder
        self.timeout = timeout

        self._session: Optional[requests.Session] = None

    @property
    def session(self) -> requests.Session:
        if not self._session:
            self._session = requests.session()
        return self._session

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        """
        :raise RetryableError, APIError, HTTPError
        """
        prefix = "/inApps/v1"
        url = urljoin(self.base_url, f"{prefix}/{path.strip('/')}")
        auth_headers = {"Authorization": f"Bearer {self.signed_token_encoder()}"}

        resp = self.session.request(method=method, url=url, headers=auth_headers, timeout=self.timeout, **kwargs)

        if resp.status_code != HTTPStatus.OK:
            if resp.status_code == HTTPStatus.UNAUTHORIZED:
                raise AuthenticationError(resp.text)
            else:
                try:
                    content = resp.json()
                    api_error = APIError(error_code=content.get("errorCode"), error_message=content.get("errorMessage"))
                    RetryableError.raise_for_api_error(api_error)
                    raise api_error
                except ValueError:
                    resp.raise_for_status()

        return resp

    def get_transaction_history(
        self, transaction_id: str, params: Optional[GetTransactionHistoryQueryParameters] = None
    ) -> HistoryResponse:
        """
        Get a customer’s in-app purchase transaction history for your app.
        https://developer.apple.com/documentation/appstoreserverapi/get_transaction_history
        """
        path = f"history/{transaction_id}"
        resp = self.request(
            method="GET", path=path, params=params.dict(exclude_none=True, by_alias=True) if params else None
        )
        return HistoryResponse.parse_obj(resp.json())

    def get_transaction_info(self, transaction_id: str) -> TransactionInfoResponse:
        """
        Get information about a single transaction for your app.
        https://developer.apple.com/documentation/appstoreserverapi/get_transaction_info
        """
        path = f"transactions/{transaction_id}"
        resp = self.request(method="GET", path=path)
        return TransactionInfoResponse.parse_obj(resp.json())

    def get_all_subscription_statuses(
        self, transaction_id: str, params: Optional[GetAllSubscriptionStatusesQueryParameters] = None
    ) -> StatusResponse:
        """
        Get the statuses for all of a customer’s auto-renewable subscriptions in your app.
        https://developer.apple.com/documentation/appstoreserverapi/get_all_subscription_statuses
        """
        path = f"subscriptions/{transaction_id}"
        resp = self.request(
            method="GET", path=path, params=params.dict(exclude_none=True, by_alias=True) if params else None
        )
        return StatusResponse.parse_obj(resp.json())

    def look_up_order_id(self, order_id: str) -> OrderLookupResponse:
        """
        Get a customer’s in-app purchases from a receipt using the order ID.
        https://developer.apple.com/documentation/appstoreserverapi/look_up_order_id
        """
        path = f"lookup/{order_id}"
        resp = self.request(method="GET", path=path)
        return OrderLookupResponse.parse_obj(resp.json())

    def request_a_test_notification(self) -> Dict[str, Any]:
        """
        Ask App Store Server Notifications to send a test notification to your server.
        https://developer.apple.com/documentation/appstoreserverapi/request_a_test_notification
        """
        path = "notifications/test"
        resp = self.request(method="POST", path=path)
        return resp.json()
