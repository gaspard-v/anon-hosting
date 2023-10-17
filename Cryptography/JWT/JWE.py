import os
from typing import Any
import time
from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode
import json


class JWEOperation:
    def __init__(self, data: dict[str, Any] | str | bytes):
        private_folder = os.environ["PRIVATE_FOLDER"]
        jwe_key_file = "jwe_key.json"
        jwe_key_path = os.path.join(private_folder, jwe_key_file)
        if not os.path.exists(private_folder):
            os.mkdir(private_folder)
        if not os.path.exists(jwe_key_path):
            self._key = jwk.JWK.generate(
                kty="oct", size=256, kid=os.environ["WEBSITE_NAME"]
            )
            with open(jwe_key_path, "w") as jwe_key_stream:
                jwe_key_stream.write(self._key.export())
        else:
            with open(jwe_key_path, "r") as jwe_key_stream:
                self._key = jwk.JWK.from_json(jwe_key_stream.read())
        epoch_time = int(time.time())
        if isinstance(data, dict):
            claims = {"iat": epoch_time, "nbf": epoch_time}
            claims.update(data)
            self._data = claims
        else:
            self._data = data

    def generate_jwt(self) -> str:
        if not isinstance(self._data, dict):
            raise ValueError("Data must be a dict")
        message = json_encode(self._data).encode()
        jwetoken = jwe.JWE(
            message, json_encode({"alg": "A256KW", "enc": "A256CBC-HS512"})
        )
        jwetoken.add_recipient(self._key)
        return jwetoken.serialize(compact=True)

    def decode_jwt(self) -> dict:
        if not isinstance(self._data, (str, bytes)):
            raise ValueError("Data must be an str or bytes")
        jwetoken = jwe.JWE()
        jwetoken.deserialize(self._data)
        jwetoken.decrypt(self._key)
        return json.loads(jwetoken.payload)
