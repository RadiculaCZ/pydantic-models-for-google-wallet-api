# https://developers.google.com/wallet/reference/rest/v1/LatLongPoint

from typing import Annotated, Literal

from pydantic import BaseModel, Field
from typing_extensions import deprecated


class LatLongPoint(BaseModel):
    kind: Annotated[
        Literal["walletobjects#latLongPoint"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#latLongPoint"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#latLongPoint"`.
    """

    latitude: float = Field(
        ge=-90.0,
        le=90.0,
    )
    """
    The latitude specified as any value in the range of -90.0 through +90.0,
    both inclusive. Values outside these bounds will be rejected.
    """

    longitude: float = Field(
        ge=-180.0,
        le=180.0,
    )
    """
    The longitude specified in the range -180.0 through +180.0, both inclusive.
    Values outside these bounds will be rejected.
    """
