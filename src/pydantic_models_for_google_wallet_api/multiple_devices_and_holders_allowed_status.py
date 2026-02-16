# https://developers.google.com/wallet/reference/rest/v1/MultipleDevicesAndHoldersAllowedStatus

from enum import Enum


class MultipleDevicesAndHoldersAllowedStatus(str, Enum):
    """
    Clarifies the issuer preference for whether Wallet should allow the same
    pass object to be shared and saved among more than one user and more than
    one device.
    """

    STATUS_UNSPECIFIED = "STATUS_UNSPECIFIED"
    """
    Unspecified preference.
    """

    MULTIPLE_HOLDERS = "MULTIPLE_HOLDERS"
    """
    The Pass object is shareable by a user and can be saved by any number of
    different users, and on any number of devices. Partners typically use this
    setup for passes that do not need to be restricted to a single user or
    pinned to a single device.
    """

    ONE_USER_ALL_DEVICES = "ONE_USER_ALL_DEVICES"
    """
    An object can only be saved by one user, but this user can view and use it
    on multiple of their devices. Once the first user saves the object, no
    other user will be allowed to view or save it.
    """

    ONE_USER_ONE_DEVICE = "ONE_USER_ONE_DEVICE"
    """
    An object can only be saved by one user on a single device. Intended for
    use by select partners in limited circumstances. An example use case is a
    transit ticket that should be "device pinned", meaning it can be saved,
    viewed and used only by a single user on a single device. Contact support
    for additional information.
    """

    multipleHolders = "multipleHolders"
    """
    Legacy alias for `MULTIPLE_HOLDERS`. Deprecated.
    """

    oneUserAllDevices = "oneUserAllDevices"
    """
    Legacy alias for `ONE_USER_ALL_DEVICES`. Deprecated.
    """

    oneUserOneDevice = "oneUserOneDevice"
    """
    Legacy alias for `ONE_USER_ONE_DEVICE`. Deprecated.
    """
