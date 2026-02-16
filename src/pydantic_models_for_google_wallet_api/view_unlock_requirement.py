# https://developers.google.com/wallet/reference/rest/v1/ViewUnlockRequirement

from enum import Enum


class ViewUnlockRequirement(str, Enum):
    """
    Defines what unlock mechanism, if any, is required to view the card.
    """

    VIEW_UNLOCK_REQUIREMENT_UNSPECIFIED = "VIEW_UNLOCK_REQUIREMENT_UNSPECIFIED"
    """
    Default value, same as UNLOCK_NOT_REQUIRED.
    """

    UNLOCK_NOT_REQUIRED = "UNLOCK_NOT_REQUIRED"
    """
    Default behavior for all the existing Passes if ViewUnlockRequirement is
    not set.
    """

    UNLOCK_REQUIRED_TO_VIEW = "UNLOCK_REQUIRED_TO_VIEW"
    """
    Requires the user to unlock their device each time the pass is viewed.

    If the user removes their device lock after saving the pass, then they will
    be prompted to create a device lock before the pass can be viewed.
    """
