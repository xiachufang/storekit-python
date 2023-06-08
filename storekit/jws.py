import abc
import base64
from typing import Any, Dict, Type, TypeVar

import jwt
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from pydantic import BaseModel

_AppleRootCA_G3 = """-----BEGIN CERTIFICATE-----
MIICQzCCAcmgAwIBAgIILcX8iNLFS5UwCgYIKoZIzj0EAwMwZzEbMBkGA1UEAwwS
QXBwbGUgUm9vdCBDQSAtIEczMSYwJAYDVQQLDB1BcHBsZSBDZXJ0aWZpY2F0aW9u
IEF1dGhvcml0eTETMBEGA1UECgwKQXBwbGUgSW5jLjELMAkGA1UEBhMCVVMwHhcN
MTQwNDMwMTgxOTA2WhcNMzkwNDMwMTgxOTA2WjBnMRswGQYDVQQDDBJBcHBsZSBS
b290IENBIC0gRzMxJjAkBgNVBAsMHUFwcGxlIENlcnRpZmljYXRpb24gQXV0aG9y
aXR5MRMwEQYDVQQKDApBcHBsZSBJbmMuMQswCQYDVQQGEwJVUzB2MBAGByqGSM49
AgEGBSuBBAAiA2IABJjpLz1AcqTtkyJygRMc3RCV8cWjTnHcFBbZDuWmBSp3ZHtf
TjjTuxxEtX/1H7YyYl3J6YRbTzBPEVoA/VhYDKX1DyxNB0cTddqXl5dvMVztK517
IDvYuVTZXpmkOlEKMaNCMEAwHQYDVR0OBBYEFLuw3qFYM4iapIqZ3r6966/ayySr
MA8GA1UdEwEB/wQFMAMBAf8wDgYDVR0PAQH/BAQDAgEGMAoGCCqGSM49BAMDA2gA
MGUCMQCD6cHEFl4aXTQY2e3v9GwOAEZLuN+yRhHFD/3meoyhpmvOwgPUnPWTxnS4
at+qIxUCMG1mihDK1A3UT82NQz60imOlM27jbdoXt2QfyFMm+YhidDkLF1vLUagM
6BgD56KyKA==
-----END CERTIFICATE-----"""

_APPLE_ROOT_CERT = x509.load_pem_x509_certificate(_AppleRootCA_G3.encode())


def decode(token: str) -> Dict[str, Any]:
    header = jwt.get_unverified_header(token)
    cert_chain = [x509.load_der_x509_certificate(base64.b64decode(key)) for key in header["x5c"]]

    if cert_chain[-1].public_bytes(serialization.Encoding.DER) != _APPLE_ROOT_CERT.public_bytes(
        serialization.Encoding.DER
    ):
        raise ValueError("Invalid certificate chain")

    for i in range(len(cert_chain) - 1):
        c = cert_chain[i]
        cert_chain[i + 1].public_key().verify(  # type: ignore
            c.signature,
            c.tbs_certificate_bytes,
            ec.ECDSA(c.signature_hash_algorithm),  # type: ignore
        )

    return jwt.decode(jwt=token, key=cert_chain[0].public_key(), algorithms=[header["alg"]])  # type: ignore


JwsT = TypeVar("JwsT", bound="BaseModel")


class JWS(BaseModel, abc.ABC):
    @classmethod
    def validate(cls: Type[JwsT], value: Any) -> JwsT:
        if isinstance(value, str):
            value = decode(value)
        return super().validate(value)
