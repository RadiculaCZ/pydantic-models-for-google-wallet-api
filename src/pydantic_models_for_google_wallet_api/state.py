# https://developers.google.com/wallet/reference/rest/v1/State

from enum import Enum


class State(str, Enum):
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    """
    Default value.
    """

    ACTIVE = "ACTIVE"
    """
    Object is active and displayed to with other active objects.
    """

    active = "active"
    """
    Legacy alias for `ACTIVE`. Deprecated.
    """

    COMPLETED = "COMPLETED"
    """
    Object has completed it's lifecycle.
    """

    completed = "completed"
    """
    Legacy alias for `COMPLETED`. Deprecated.
    """

    EXPIRED = "EXPIRED"
    """
    Object is no longer valid (`validTimeInterval` passed).
    """

    expired = "expired"
    """
    Legacy alias for `EXPIRED`. Deprecated.
    """

    INACTIVE = "INACTIVE"
    """
    Object is no longer valid
    """

    inactive = "inactive"
    """
    Legacy alias for `INACTIVE`. Deprecated.
    """
