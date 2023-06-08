import base64
import datetime
import uuid
from typing import Any, Dict
from unittest import mock

import jwt
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID


class JwsMocker:
    def __init__(self):
        root_key, root_certificate = self.create_root_certificate()
        child_key_a, child_certificate_a = self.create_child_certificate(root_key, root_certificate)
        child_key_b, child_certificate_b = self.create_child_certificate(child_key_a, child_certificate_a)

        self.root_certificate = root_certificate
        self.private_key = child_key_b

        self.headers = {
            "alg": "ES256",
            "x5c": [
                base64.b64encode(child_certificate_b.public_bytes(serialization.Encoding.DER)).decode(),
                base64.b64encode(child_certificate_a.public_bytes(serialization.Encoding.DER)).decode(),
                base64.b64encode(root_certificate.public_bytes(serialization.Encoding.DER)).decode(),
            ],
        }

        self.apple_root_cert_patcher = mock.patch("storekit.jws._APPLE_ROOT_CERT", self.root_certificate)

    def encode(self, payload: Dict[str, Any]) -> str:
        return jwt.encode(payload, self.private_key, algorithm="ES256", headers=self.headers)

    def __enter__(self):
        self.apple_root_cert_patcher.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.apple_root_cert_patcher.stop()

    @staticmethod
    def create_root_certificate():
        key = ec.generate_private_key(ec.SECP256R1())

        name = x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, "My Root CA"),
            ]
        )
        basic_constraints = x509.BasicConstraints(ca=True, path_length=None)
        now = datetime.datetime.utcnow()
        subject_key_identifier = x509.SubjectKeyIdentifier.from_public_key(key.public_key())

        certificate = (
            x509.CertificateBuilder()
            .subject_name(name)
            .issuer_name(name)
            .not_valid_before(now)
            .not_valid_after(now + datetime.timedelta(days=365))
            .serial_number(int(uuid.uuid4()))
            .public_key(key.public_key())
            .add_extension(basic_constraints, False)
            .add_extension(subject_key_identifier, False)
            .sign(key, hashes.SHA256())
        )

        return key, certificate

    @staticmethod
    def create_child_certificate(ca_key, ca_cert):
        key = ec.generate_private_key(ec.SECP256R1())

        name = x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, "My Child Certificate"),
            ]
        )
        now = datetime.datetime.utcnow()
        certificate = (
            x509.CertificateBuilder()
            .subject_name(name)
            .issuer_name(ca_cert.subject)
            .not_valid_before(now)
            .not_valid_after(now + datetime.timedelta(days=365))
            .serial_number(int(uuid.uuid4()))
            .public_key(key.public_key())
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), False)
            .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), False)
            .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_cert.public_key()), False)
            .sign(ca_key, hashes.SHA256())
        )

        return key, certificate


@pytest.fixture
def jws_mocker():
    with JwsMocker() as mocker:
        yield mocker
