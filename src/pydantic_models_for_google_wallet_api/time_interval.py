# https://developers.google.com/wallet/reference/rest/v1/TimeInterval

from typing import Annotated, Literal, Optional

from pydantic import BaseModel
from typing_extensions import deprecated

from .date_time import DateTime


class TimeInterval(BaseModel):
    kind: Annotated[
        Literal["walletobjects#timeInterval"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#timeInterval"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#timeInterval"`.
    """

    start: Optional[DateTime] = None
    """
    Start time of the interval.

    Offset is not required. If an offset is provided and `end` time is set,
    `end` must also include an offset.
    """

    end: Optional[DateTime] = None
    """
    End time of the interval.

    Offset is not required. If an offset is provided and `start` time is set,
    `start` must also include an offset.
    """
