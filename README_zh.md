# storekit-python

[![pypi](https://img.shields.io/pypi/v/storekit-python.svg)](https://pypi.python.org/pypi/storekit-python)
[![versions](https://img.shields.io/pypi/pyversions/storekit-python.svg)](https://github.com/xiachufang/storekit-python)
[![license](https://img.shields.io/github/license/xiachufang/storekit-python.svg)](https://github.com/xiachufang/storekit-python/blob/main/LICENSE)

storekit-python 是一个用于访问和验证 App Store 内购的 Python 包。

## 目录

- [安装方法](#安装方法)
- [如何使用](#如何使用)
    - [App Store Server API](#app-store-server-api)
    - [App Store Server Notifications](#app-store-server-notifications)
    - [App Store Receipts](#app-store-receipts)
- [贡献](#贡献)
- [许可证](#许可证)

## 安装方法

使用 pip 进行安装:

```bash
pip install storekit-python
```

## Quick Start

### App Store Server API

获取 SignedTokenEncoder 参数参考：[Generating tokens for API requests](https://developer.apple.com/documentation/appstoreserverapi/generating_tokens_for_api_requests)

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

[启用App Store服务器通知](https://developer.apple.com/documentation/appstoreservernotifications/enabling_app_store_server_notifications)

```python
from storekit.app_store_server_notifications import ResponseBodyV2

response = ResponseBodyV2.parse_obj(request_data)
print(response)
```

### App Store Receipts

如何生成 password 参考：[Generating a Shared Secret](https://developer.apple.com/help/app-store-connect/configure-in-app-purchase-settings/generate-a-shared-secret-to-verify-receipts)

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

## 贡献

我们欢迎各种形式的贡献！你可以通过报告 issues、提交 PRs 或者改进文档等来参与这个项目。

## 许可证

storekit-python 采用 [MIT License](https://github.com/xiachufang/storekit-python/blob/main/LICENSE) 开源。
