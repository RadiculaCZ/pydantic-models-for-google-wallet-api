# https://developers.google.com/wallet/reference/rest/v1/SecurityAnimation

from enum import Enum

from pydantic import BaseModel


class AnimationType(str, Enum):
    ANIMATION_UNSPECIFIED = "ANIMATION_UNSPECIFIED"

    FOIL_SHIMMER = "FOIL_SHIMMER"
    """
    Default Foil & Shimmer animation
    """

    foilShimmer = "foilShimmer"
    """
    Legacy alias for `FOIL_SHIMMER`. Deprecated.
    """


class SecurityAnimation(BaseModel):
    animationType: AnimationType = AnimationType.ANIMATION_UNSPECIFIED
    """
    Type of animation.
    """
