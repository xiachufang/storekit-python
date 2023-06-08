from pydantic import BaseModel

from storekit import jws


def test_jws_decode(jws_mocker):
    token = jws_mocker.encode({"a": 1})
    assert jws.decode(token) == {"a": 1}


class JwsPayload(jws.JWS):
    a: int
    b: str


class Response(BaseModel):
    jws_payload: JwsPayload


def test_jws_model(jws_mocker):
    response_data = {"jws_payload": jws_mocker.encode({"a": 1, "b": "2"})}
    response = Response.parse_obj(response_data)
    assert response.jws_payload.a == 1
    assert response.jws_payload.b == "2"
