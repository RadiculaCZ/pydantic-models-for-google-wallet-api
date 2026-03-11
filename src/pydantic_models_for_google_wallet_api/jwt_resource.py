# https://developers.google.com/wallet/reference/rest/v1/jwt

from typing import Optional

from pydantic import BaseModel


class JwtResource(BaseModel):
    jwt: Optional[str] = None
    """
    A string representing a JWT of the format described at
    https://developers.google.com/wallet/reference/rest/v1/Jwt

    See the `JWT` class.
    """
