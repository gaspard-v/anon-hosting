from Exceptions import EnvVariableNotDefined
from typing import Any
import time
import jwt
import os


class JWSOperation:
    def __init__(self, data: dict[str, Any] | str | bytes):
        if not os.environ.get("SECRET_KEY"):
            raise EnvVariableNotDefined("SECRET_KEY")
        self._key = os.environ["SECRET_KEY"]
        self._algorithm = "HS256"
        self._options = {
            "verify_signature": True,
            "require": ["iat", "nbf"],
            "verify_nbf": "verify_signature",
        }
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
        return jwt.encode(self._data, key=self._key, algorithm=self._algorithm)

    def decode_jwt(self):
        if not isinstance(self._data, (str, bytes)):
            raise ValueError("Data must be an str or bytes")
        return jwt.decode(
            self._data,
            key=self._key,
            algorithm=self._algorithm,
            options=self._options,
        )
