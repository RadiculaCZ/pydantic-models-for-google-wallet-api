# https://developers.google.com/wallet/reference/rest/v1/NotificationSettingsForUpdates

from enum import Enum


class NotificationSettingsForUpdates(str, Enum):
    """
    Whether or not field updates to this class should trigger notifications.
    When set to NOTIFY, we will attempt to trigger a field update notification
    to users. These notifications will only be sent to users if the field is
    part of an allowlist. If not specified, no notification will be triggered.
    This setting is ephemeral and needs to be set with each PATCH or UPDATE
    request, otherwise a notification will not be triggered.
    """

    NOTIFICATION_SETTINGS_FOR_UPDATES_UNSPECIFIED = (
        "NOTIFICATION_SETTINGS_FOR_UPDATES_UNSPECIFIED"
    )
    """
    Default behavior is no notifications sent.
    """

    NOTIFY_ON_UPDATE = "NOTIFY_ON_UPDATE"
    """
    This value will result in a notification being sent, if the updated fields
    are part of an allowlist.
    """
