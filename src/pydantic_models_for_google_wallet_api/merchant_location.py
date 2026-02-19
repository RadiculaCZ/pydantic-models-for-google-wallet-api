# https://developers.google.com/wallet/reference/rest/v1/MerchantLocation

from pydantic import BaseModel, Field


class MerchantLocation(BaseModel):
    """
    Locations of interest for this class or object. Currently, this location is
    used for geofenced notifications. When a user is within a set radius of
    this lat/long, and dwells there, Google will trigger a notification. When a
    user exits this radius, the notification will be hidden.
    """

    latitude: float = Field(
        ...,
        ge=-90.0,
        le=90.0,
    )
    """
    The latitude specified as any value in the range of -90.0 through +90.0,
    both inclusive. Values outside these bounds will be rejected.
    """

    longitude: float = Field(
        ...,
        ge=-180.0,
        le=180.0,
    )
    """
    The longitude specified in the range -180.0 through +180.0, both inclusive.
    Values outside these bounds will be rejected.
    """
