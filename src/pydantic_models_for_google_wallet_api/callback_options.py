# https://developers.google.com/wallet/reference/rest/v1/CallbackOptions

from typing import Annotated, Optional

from pydantic import BaseModel
from typing_extensions import deprecated


class CallbackOptions(BaseModel):
    url: str
    """
    The HTTPS url configured by the merchant. The URL should be hosted on HTTPS
    and robots.txt should allow the URL path to be accessible by
    UserAgent:Googlebot.
    """

    updateRequestUrl: Annotated[
        Optional[str],
        deprecated("This item is deprecated!"),
    ] = None
    """
    URL for the merchant endpoint that would be called to request updates. The
    URL should be hosted on HTTPS and robots.txt should allow the URL path to
    be accessible by UserAgent:Googlebot. Deprecated.
    """
