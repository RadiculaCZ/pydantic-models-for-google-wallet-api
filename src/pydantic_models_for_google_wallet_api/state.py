# https://developers.google.com/wallet/reference/rest/v1/State

from enum import Enum


class State(Enum):
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"

    ACTIVE = "ACTIVE"
    """
    Object is active and displayed to with other active objects.
    """

    active = "active"
    """
    Legacy alias for `ACTIVE`. Deprecated.
    """

    COMPLETED = "COMPLETED"

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

    inactive = "inactive"
    """
    Legacy alias for `INACTIVE`. Deprecated.
    """
