# storekit-python

[![pypi](https://img.shields.io/pypi/v/storekit-python.svg)](https://pypi.python.org/pypi/storekit-python)
[![versions](https://img.shields.io/pypi/pyversions/storekit-python.svg)](https://github.com/xiachufang/storekit-python)
[![license](https://img.shields.io/github/license/xiachufang/storekit-python.svg)](https://github.com/xiachufang/storekit-python/blob/main/LICENSE)

[简体中文](https://github.com/xiachufang/storekit-python/blob/main/README_zh.md)

storekit-python is a Python package for accessing and validating App Store in-app purchases.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
    - [App Store Server API](#app-store-server-api)
    - [App Store Server Notifications](#app-store-server-notifications)
    - [App Store Receipts](#app-store-receipts)
- [Contributing](#contributing)
- [License](#license)

## Installation

Install via pip:

```bash
pip install storekit-python
```

## Quick Start

### App Store Server API

Get SignedTokenEncoder parameters reference: [Generating tokens for API requests](https://developer.apple.com/documentation/appstoreserverapi/generating_tokens_for_api_requests)

```python
from storekit.app_store_server_api import BaseUrl, SignedTokenEncoder, ServerAPIClient

client = ServerAPIClient(
  base_url=BaseUrl.Production,
  signed_token_encoder=SignedTokenEncoder(
    key_id="key_id",
    private_key="private_key",
    issuer_id="issuer_id",
    bundle_id="bundle_id",
  )
)

response = client.get_all_subscription_statuses("original_transaction_id")
print(response)
```

### App Store Server Notifications

[Enabling App Store Server Notifications](https://developer.apple.com/documentation/appstoreservernotifications/enabling_app_store_server_notifications)

```python
from storekit.app_store_server_notifications import ResponseBodyV2

response = ResponseBodyV2.parse_obj(request_data)
print(response)
```

### App Store Receipts

How to generate a password reference: [Generating a Shared Secret](https://developer.apple.com/help/app-store-connect/configure-in-app-purchase-settings/generate-a-shared-secret-to-verify-receipts)

```python
from storekit.app_store_receipts import ReceiptsClient, BaseUrl

client = ReceiptsClient(
    base_url=BaseUrl.Production,
    password="password",
    sandbox_client=ReceiptsClient(
        base_url=BaseUrl.Sandbox,
        password="password",
    )
)

response = client.verify_receipt("receipt_data")
print(response)
```

## Contributing

We welcome contributions of all forms! You can participate in this project by reporting issues, submitting PRs, or improving documentation.

## License

storekit-python is open-source under the [MIT License](https://github.com/xiachufang/storekit-python/blob/main/LICENSE).
