from http import HTTPStatus
from typing import Any, Optional, Tuple
from urllib.parse import urljoin

import requests

from storekit.utils.enum import StrEnum

from .exceptions import APIError, RetryableError
from .verify_receipt_response import ResponseBody


class BaseUrl(StrEnum):
    Production = "https://buy.itunes.apple.com"
    Sandbox = "https://sandbox.itunes.apple.com"


class ReceiptsClient:
    STATUS_SANDBOX_RECEIPT_ERROR = 21007

    def __init__(
        self, base_url: str, password: str, sandbox_client: Optional["ReceiptsClient"] = None, timeout: int = 20
    ):
        self.base_url = base_url
        self.password = password
        self.sandbox_client = sandbox_client

        self.timeout = timeout
        self._session: Optional[requests.Session] = None

    @property
    def session(self) -> requests.Session:
        if not self._session:
            self._session = requests.session()
        return self._session

    def request(self, method: str, path: str, **kwargs: Any) -> Tuple[requests.Response, Any]:
        """
        :raise RetryableError, APIError, HTTPError
        """
        url = urljoin(self.base_url, path)
        resp = self.session.request(method=method, url=url, timeout=self.timeout, **kwargs)

        if resp.status_code != HTTPStatus.OK:
            resp.raise_for_status()

        content = resp.json()

        status: int = content.get("status")
        if status != 0:
            RetryableError.raise_for_status(status)
            raise APIError(status)

        return resp, content

    def verify_receipt(self, receipt_data: str, exclude_old_transactions: bool = False) -> ResponseBody:
        """
        Send a receipt to the App Store for verification.
        https://developer.apple.com/documentation/appstorereceipts/verifyreceipt
        """

        payload = {
            "receipt-data": receipt_data,
            "password": self.password,
            "exclude-old-transactions": exclude_old_transactions,
        }
        path = "verifyReceipt"
        try:
            resp, content = self.request(method="POST", path=path, json=payload)
        except APIError as e:
            if not (self.sandbox_client and e.status == self.STATUS_SANDBOX_RECEIPT_ERROR):
                raise
            resp, content = self.sandbox_client.request(method="POST", path=path, json=payload)

        return ResponseBody.parse_obj(content)
