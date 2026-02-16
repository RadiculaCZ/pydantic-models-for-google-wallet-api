# https://developers.google.com/wallet/reference/rest/v1/Message

from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel
from typing_extensions import deprecated

from .localized_string import LocalizedString
from .time_interval import TimeInterval


class MessageType(str, Enum):
    MESSAGE_TYPE_UNSPECIFIED = "MESSAGE_TYPE_UNSPECIFIED"

    TEXT = "TEXT"
    """
    Renders the message as text on the card details screen. This is the default
    message type.
    """

    text = "text"
    """
    Legacy alias for `TEXT`. Deprecated.
    """

    EXPIRATION_NOTIFICATION = "EXPIRATION_NOTIFICATION"
    """
    Note: This enum is currently not supported.
    """

    expirationNotification = "expirationNotification"
    """
    Legacy alias for `EXPIRATION_NOTIFICATION`. Deprecated.
    """

    TEXT_AND_NOTIFY = "TEXT_AND_NOTIFY"
    """
    Renders the message as text on the card details screen and as an Android
    notification.
    """


class Message(BaseModel):
    """
    A message that will be displayed with a Valuable.
    """

    kind: Annotated[
        Literal["walletobjects#walletObjectMessage"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#walletObjectMessage"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#walletObjectMessage"`.
    """

    header: str
    """
    The message header.
    """

    body: str
    """
    The message body.
    """

    displayInterval: TimeInterval
    """
    The period of time that the message will be displayed to users. You can
    define both a `startTime` and `endTime` for each message. A message is
    displayed immediately after a Wallet Object is inserted unless a
    `startTime` is set. The message will appear in a list of messages
    indefinitely if `endTime` is not provided.
    """

    id: str
    """
    The ID associated with a message. This field is here to enable ease of
    management of messages. Notice ID values could possibly duplicate across
    multiple messages in the same class/instance, and care must be taken to
    select a reasonable ID for each message.
    """

    messageType: MessageType = MessageType.MESSAGE_TYPE_UNSPECIFIED
    """
    The message type.
    """

    localizedHeader: LocalizedString
    """
    Translated strings for the message header.
    """

    localizedBody: LocalizedString
    """
    Translated strings for the message body.
    """
