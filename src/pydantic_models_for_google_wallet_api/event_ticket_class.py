# https://developers.google.com/wallet/reference/rest/v1/eventticketclass

from enum import Enum
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field
from typing_extensions import deprecated

from .app_link_data import AppLinkData
from .callback_options import CallbackOptions
from .class_template_info import ClassTemplateInfo
from .image import Image
from .image_module_data import ImageModuleData
from .info_module_data import InfoModuleData
from .lat_long_point import LatLongPoint
from .links_module_data import LinksModuleData
from .localized_string import LocalizedString
from .merchant_location import MerchantLocation
from .message import Message
from .multiple_devices_and_holders_allowed_status import (
    MultipleDevicesAndHoldersAllowedStatus,
)
from .notification_settings_for_updates import NotificationSettingsForUpdates
from .review import Review
from .review_status import ReviewStatus
from .security_animation import SecurityAnimation
from .text_module_data import TextModuleData
from .uri import Uri
from .value_added_module_data import ValueAddedModuleData
from .view_unlock_requirement import ViewUnlockRequirement


class EventVenue(BaseModel):
    kind: Annotated[
        Literal["walletobjects#eventVenue"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#eventVenue"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#eventVenue"`.
    """

    name: LocalizedString
    """
    The name of the venue, such as "AT&T Park".

    This is required.
    """

    address: LocalizedString
    """
    The address of the venue, such as "24 Willie Mays Plaza\nSan Francisco, CA
    94107". Address lines are separated by line feed (`\n`) characters.

    This is required.
    """


class DoorsOpenLabel(str, Enum):
    DOORS_OPEN_LABEL_UNSPECIFIED = "DOORS_OPEN_LABEL_UNSPECIFIED"

    DOORS_OPEN = "DOORS_OPEN"

    doorsOpen = "doorsOpen"
    """
    Legacy alias for `DOORS_OPEN`. Deprecated.
    """

    GATES_OPEN = "GATES_OPEN"

    gatesOpen = "gatesOpen"
    """
    Legacy alias for `GATES_OPEN`. Deprecated.
    """


class ConfirmationCodeLabel(str, Enum):
    CONFIRMATION_CODE_LABEL_UNSPECIFIED = "CONFIRMATION_CODE_LABEL_UNSPECIFIED"

    CONFIRMATION_CODE = "CONFIRMATION_CODE"

    confirmationCode = "confirmationCode"
    """
    Legacy alias for `CONFIRMATION_CODE`. Deprecated.
    """

    CONFIRMATION_NUMBER = "CONFIRMATION_NUMBER"

    confirmationNumber = "confirmationNumber"
    """
    Legacy alias for `CONFIRMATION_NUMBER`. Deprecated.
    """

    ORDER_NUMBER = "ORDER_NUMBER"

    orderNumber = "orderNumber"
    """
    Legacy alias for `ORDER_NUMBER`. Deprecated.
    """

    RESERVATION_NUMBER = "RESERVATION_NUMBER"

    reservationNumber = "reservationNumber"
    """
    Legacy alias for `RESERVATION_NUMBER`. Deprecated.
    """


class SeatLabel(str, Enum):
    SEAT_LABEL_UNSPECIFIED = "SEAT_LABEL_UNSPECIFIED"

    SEAT = "SEAT"

    seat = "seat"
    """
    Legacy alias for `SEAT`. Deprecated.
    """


class RowLabel(str, Enum):
    ROW_LABEL_UNSPECIFIED = "ROW_LABEL_UNSPECIFIED"

    ROW = "ROW"

    row = "row"
    """
    Legacy alias for `ROW`. Deprecated.
    """


class SectionLabel(str, Enum):
    SECTION_LABEL_UNSPECIFIED = "SECTION_LABEL_UNSPECIFIED"

    SECTION = "SECTION"

    section = "section"
    """
    Legacy alias for `SECTION`. Deprecated.
    """

    THEATER = "THEATER"

    theater = "theater"
    """
    Legacy alias for `THEATER`. Deprecated.
    """


class GateLabel(str, Enum):
    GATE_LABEL_UNSPECIFIED = "GATE_LABEL_UNSPECIFIED"

    GATE = "GATE"

    gate = "gate"
    """
    Legacy alias for `GATE`. Deprecated.
    """

    DOOR = "DOOR"

    door = "door"
    """
    Legacy alias for `DOOR`. Deprecated.
    """

    ENTRANCE = "ENTRANCE"

    entrance = "entrance"
    """
    Legacy alias for `ENTRANCE`. Deprecated.
    """


class EventDateTime(BaseModel):
    kind: Annotated[
        Literal["walletobjects#eventDateTime"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#eventDateTime"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#eventDateTime"`.
    """

    doorsOpen: Optional[str] = None
    """
    The date/time when the doors open at the venue.

    This is an ISO 8601 extended format date/time, with or without an offset.
    Time may be specified up to nanosecond precision. Offsets may be specified
    with seconds precision (even though offset seconds is not part of ISO
    8601).

    For example:

    `1985-04-12T23:20:50.52Z` would be 20 minutes and 50.52 seconds after the
    23rd hour of April 12th, 1985 in UTC.

    `1985-04-12T19:20:50.52-04:00` would be 20 minutes and 50.52 seconds after
    the 19th hour of April 12th, 1985, 4 hours before UTC (same instant in time
    as the above example). If the event were in New York, this would be the
    equivalent of Eastern Daylight Time (EDT). Remember that offset varies in
    regions that observe Daylight Saving Time (or Summer Time), depending on
    the time of the year.

    `1985-04-12T19:20:50.52` would be 20 minutes and 50.52 seconds after the
    19th hour of April 12th, 1985 with no offset information.

    The portion of the date/time without the offset is considered the "local
    date/time". This should be the local date/time at the venue. For example,
    if the event occurs at the 20th hour of June 5th, 2018 at the venue, the
    local date/time portion should be `2018-06-05T20:00:00`. If the local
    date/time at the venue is 4 hours before UTC, an offset of `-04:00` may be
    appended.

    Without offset information, some rich features may not be available.
    """

    start: Optional[str] = None
    """
    The date/time when the event starts. If the event spans multiple days, it
    should be the start date/time on the first day.

    This is an ISO 8601 extended format date/time, with or without an offset.
    Time may be specified up to nanosecond precision. Offsets may be specified
    with seconds precision (even though offset seconds is not part of ISO
    8601).

    For example:

    `1985-04-12T23:20:50.52Z` would be 20 minutes and 50.52 seconds after the
    23rd hour of April 12th, 1985 in UTC.

    `1985-04-12T19:20:50.52-04:00` would be 20 minutes and 50.52 seconds after
    the 19th hour of April 12th, 1985, 4 hours before UTC (same instant in time
    as the above example). If the event were in New York, this would be the
    equivalent of Eastern Daylight Time (EDT). Remember that offset varies in
    regions that observe Daylight Saving Time (or Summer Time), depending on
    the time of the year.

    `1985-04-12T19:20:50.52` would be 20 minutes and 50.52 seconds after the
    19th hour of April 12th, 1985 with no offset information.

    The portion of the date/time without the offset is considered the "local
    date/time". This should be the local date/time at the venue. For example,
    if the event occurs at the 20th hour of June 5th, 2018 at the venue, the
    local date/time portion should be `2018-06-05T20:00:00`. If the local
    date/time at the venue is 4 hours before UTC, an offset of `-04:00` may be
    appended.

    Without offset information, some rich features may not be available.
    """

    end: Optional[str] = None
    """
    The date/time when the event ends. If the event spans multiple days, it
    should be the end date/time on the last day.

    This is an ISO 8601 extended format date/time, with or without an offset.
    Time may be specified up to nanosecond precision. Offsets may be specified
    with seconds precision (even though offset seconds is not part of ISO
    8601).

    For example:

    `1985-04-12T23:20:50.52Z` would be 20 minutes and 50.52 seconds after the
    23rd hour of April 12th, 1985 in UTC.

    `1985-04-12T19:20:50.52-04:00` would be 20 minutes and 50.52 seconds after
    the 19th hour of April 12th, 1985, 4 hours before UTC (same instant in time
    as the above example). If the event were in New York, this would be the
    equivalent of Eastern Daylight Time (EDT). Remember that offset varies in
    regions that observe Daylight Saving Time (or Summer Time), depending on
    the time of the year.

    `1985-04-12T19:20:50.52` would be 20 minutes and 50.52 seconds after the
    19th hour of April 12th, 1985 with no offset information.

    The portion of the date/time without the offset is considered the "local
    date/time". This should be the local date/time at the venue. For example,
    if the event occurs at the 20th hour of June 5th, 2018 at the venue, the
    local date/time portion should be `2018-06-05T20:00:00`. If the local
    date/time at the venue is 4 hours before UTC, an offset of `-04:00` may be
    appended.

    Without offset information, some rich features may not be available.
    """

    doorsOpenLabel: DoorsOpenLabel = (
        DoorsOpenLabel.DOORS_OPEN_LABEL_UNSPECIFIED
    )
    """
    The label to use for the doors open value (`doorsOpen`) on the card detail
    view. Each available option maps to a set of localized strings, so that
    translations are shown to the user based on their locale.

    Both `doorsOpenLabel` and `customDoorsOpenLabel` may not be set. If neither
    is set, the label will default to "Doors Open", localized. If the doors
    open field is unset, this label will not be used.
    """

    customDoorsOpenLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the doors open value (`doorsOpen`) on the card
    detail view. This should only be used if the default "Doors Open" label or
    one of the `doorsOpenLabel` options is not sufficient.

    Both `doorsOpenLabel` and `customDoorsOpenLabel` may not be set. If neither
    is set, the label will default to "Doors Open", localized. If the doors
    open field is unset, this label will not be used.
    """


class EventTicketClass(BaseModel):
    kind: Annotated[
        Literal["walletobjects#eventTicketClass"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#eventTicketClass"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#eventTicketClass"`.
    """

    eventName: LocalizedString
    """
    Required. The name of the event, such as "LA Dodgers at SF Giants".
    """

    eventId: Optional[str] = Field(
        max_length=64,
    )
    """
    The ID of the event. This ID should be unique for every event in an
    account. It is used to group tickets together if the user has saved
    multiple tickets for the same event. It can be at most 64 characters.

    If provided, the grouping will be stable. Be wary of unintentional
    collision to avoid grouping tickets that should not be grouped. If you use
    only one class per event, you can simply set this to the `classId` (with or
    without the issuer ID portion).

    If not provided, the platform will attempt to use other data to group
    tickets (potentially unstable).
    """

    logo: Image
    """
    The logo image of the ticket. This image is displayed in the card detail
    view of the app.
    """

    venue: EventVenue
    """
    Event venue details.
    """

    dateTime: EventDateTime
    """
    The date & time information of the event.
    """

    confirmationCodeLabel: ConfirmationCodeLabel = (
        ConfirmationCodeLabel.CONFIRMATION_CODE_LABEL_UNSPECIFIED
    )
    """
    The label to use for the confirmation code value
    (`eventTicketObject.reservationInfo.confirmationCode`) on the card detail
    view. Each available option maps to a set of localized strings, so that
    translations are shown to the user based on their locale.

    Both `confirmationCodeLabel` and `customConfirmationCodeLabel` may not be
    set. If neither is set, the label will default to "Confirmation Code",
    localized. If the confirmation code field is unset, this label will not be
    used.
    """

    customConfirmationCodeLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the confirmation code value
    (`eventTicketObject.reservationInfo.confirmationCode`) on the card detail
    view. This should only be used if the default "Confirmation Code" label or
    one of the `confirmationCodeLabel` options is not sufficient.

    Both `confirmationCodeLabel` and `customConfirmationCodeLabel` may not be
    set. If neither is set, the label will default to "Confirmation Code",
    localized. If the confirmation code field is unset, this label will not be
    used.
    """

    seatLabel: SeatLabel = SeatLabel.SEAT_LABEL_UNSPECIFIED
    """
    The label to use for the seat value (`eventTicketObject.seatInfo.seat`) on
    the card detail view. Each available option maps to a set of localized
    strings, so that translations are shown to the user based on their locale.

    Both `seatLabel` and `customSeatLabel` may not be set. If neither is set,
    the label will default to "Seat", localized. If the seat field is unset,
    this label will not be used.
    """

    customSeatLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the seat value
    (`eventTicketObject.seatInfo.seat`) on the card detail view. This should
    only be used if the default "Seat" label or one of the `seatLabel` options
    is not sufficient.

    Both `seatLabel` and `customSeatLabel` may not be set. If neither is set,
    the label will default to "Seat", localized. If the seat field is unset,
    this label will not be used.
    """

    rowLabel: RowLabel = RowLabel.ROW_LABEL_UNSPECIFIED
    """
    The label to use for the row value (`eventTicketObject.seatInfo.row`) on
    the card detail view. Each available option maps to a set of localized
    strings, so that translations are shown to the user based on their locale.

    Both `rowLabel` and `customRowLabel` may not be set. If neither is set, the
    label will default to "Row", localized. If the row field is unset, this
    label will not be used.
    """

    customRowLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the row value (`eventTicketObject.seatInfo.row`)
    on the card detail view. This should only be used if the default "Row"
    label or one of the `rowLabel` options is not sufficient.

    Both `rowLabel` and `customRowLabel` may not be set. If neither is set, the
    label will default to "Row", localized. If the row field is unset, this
    label will not be used.
    """

    sectionLabel: SectionLabel = SectionLabel.SECTION_LABEL_UNSPECIFIED
    """
    The label to use for the section value
    (`eventTicketObject.seatInfo.section`) on the card detail view. Each
    available option maps to a set of localized strings, so that translations
    are shown to the user based on their locale.

    Both `sectionLabel` and `customSectionLabel` may not be set. If neither is
    set, the label will default to "Section", localized. If the section field
    is unset, this label will not be used.
    """

    customSectionLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the section value
    (`eventTicketObject.seatInfo.section`) on the card detail view. This should
    only be used if the default "Section" label or one of the `sectionLabel`
    options is not sufficient.

    Both `sectionLabel` and `customSectionLabel` may not be set. If neither is
    set, the label will default to "Section", localized. If the section field
    is unset, this label will not be used.
    """

    gateLabel: GateLabel = GateLabel.GATE_LABEL_UNSPECIFIED
    """
    The label to use for the gate value (`eventTicketObject.seatInfo.gate`) on
    the card detail view. Each available option maps to a set of localized
    strings, so that translations are shown to the user based on their locale.

    Both `gateLabel` and `customGateLabel` may not be set. If neither is set,
    the label will default to "Gate", localized. If the gate field is unset,
    this label will not be used.
    """

    customGateLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the gate value
    (`eventTicketObject.seatInfo.gate`) on the card detail view. This should
    only be used if the default "Gate" label or one of the `gateLabel` options
    is not sufficient.

    Both `gateLabel` and `customGateLabel` may not be set. If neither is set,
    the label will default to "Gate", localized. If the gate field is unset,
    this label will not be used.
    """

    finePrint: Optional[LocalizedString] = None
    """
    The fine print, terms, or conditions of the ticket.
    """

    classTemplateInfo: Optional[ClassTemplateInfo] = None
    """
    Template information about how the class should be displayed. If unset,
    Google will fallback to a default set of fields to display.
    """

    id: str
    """
    Required. The unique identifier for a class. This ID must be unique across
    all classes from an issuer. This value should follow the format
    `issuer ID`.`identifier` where the former is issued by Google and latter is
    chosen by you. Your unique identifier should only include alphanumeric
    characters, '.', '_', or '-'.
    """

    version: Annotated[
        Optional[str],
        deprecated("This item is deprecated!"),
    ] = None
    """
    int64 format

    Deprecated
    """

    issuerName: str = Field(
        max_length=20,
    )
    """
    Required. The issuer name. Recommended maximum length is 20 characters to
    ensure full string is displayed on smaller screens.
    """

    messages: list[Message] = Field(
        default_factory=list,
        max_length=10,
    )
    """
    An array of messages displayed in the app. All users of this object will
    receive its associated messages. The maximum number of these fields is 10.
    """

    allowMultipleUsersPerObject: Annotated[
        Optional[bool], deprecated("This item is deprecated!")
    ] = None
    """
    Deprecated. Use `multipleDevicesAndHoldersAllowedStatus` instead.
    """

    homepageUri: Optional[Uri] = None
    """
    The URI of your application's home page. Populating the URI in this field
    results in the exact same behavior as populating an URI in linksModuleData
    (when an object is rendered, a link to the homepage is shown in what would
    usually be thought of as the linksModuleData section of the object).
    """

    locations: Annotated[
        Optional[list[LatLongPoint]],
        deprecated("This item is deprecated!"),
    ] = None
    """
    Note: This field is currently not supported to trigger geo notifications.
    """

    reviewStatus: ReviewStatus
    """
    Required. The status of the class. This field can be set to `draft` or
    `underReview` using the insert, patch, or update API calls. Once the
    review state is changed from `draft` it may not be changed back to `draft`.

    You should keep this field to `draft` when the class is under development.
    A `draft` class cannot be used to create any object.

    You should set this field to `underReview` when you believe the class is
    ready for use. The platform will automatically set this field to `approved`
    and it can be immediately used to create or migrate objects.

    When updating an already approved class you should keep setting this field
    to `underReview`.
    """

    review: Optional[Review] = None
    """
    The review comments set by the platform when a class is marked `approved`
    or `rejected`.
    """

    infoModuleData: Annotated[
        Optional[InfoModuleData],
        deprecated("This item is deprecated!"),
    ] = None
    """
    Deprecated. Use textModulesData instead.
    """

    imageModulesData: list[ImageModuleData] = Field(
        default_factory=list,
    )
    """
    Image module data. The maximum number of these fields displayed is 1 from
    object level and 1 for class object level.
    """

    textModulesData: list[TextModuleData] = Field(
        default_factory=list,
    )
    """
    Text module data. If text module data is also defined on the class, both
    will be displayed. The maximum number of these fields displayed is 10 from
    the object and 10 from the class.
    """

    linksModuleData: list[LinksModuleData] = Field(
        default_factory=list,
    )
    """
    Links module data. If links module data is also defined on the object, both
    will be displayed.
    """

    redemptionIssuers: list[str] = Field(
        default_factory=list,
    )
    """
    int64 format)

    Identifies which redemption issuers can redeem the pass over Smart Tap.
    Redemption issuers are identified by their issuer ID. Redemption issuers
    must have at least one Smart Tap key configured.

    The `enableSmartTap` and object level `smartTapRedemptionLevel` fields must
    also be set up correctly in order for a pass to support Smart Tap.
    """

    countryCode: Optional[str] = None
    """
    Country code used to display the card's country (when the user is not in
    that country), as well as to display localized content when content is not
    available in the user's locale.
    """

    heroImage: Optional[Image] = None
    """
    Optional banner image displayed on the front of the card. If none is
    present, nothing will be displayed. The image will display at 100% width.
    """

    wordMark: Annotated[
        Optional[Image],
        deprecated("This item is deprecated!"),
    ] = None
    """
    Deprecated.
    """

    enableSmartTap: bool = False
    """
    Identifies whether this class supports Smart Tap. The `redemptionIssuers`
    and object level `smartTapRedemptionLevel` fields must also be set up
    correctly in order for a pass to support Smart Tap.
    """

    hexBackgroundColor: Optional[str] = None
    """
    The background color for the card. If not set the dominant color of the
    hero image is used, and if no hero image is set, the dominant color of the
    logo is used. The format is `#rrggbb` where `rrggbb` is a hex RGB triplet,
    such as `#ffcc00`. You can also use the shorthand version of the RGB
    triplet which is `#rgb`, such as `#fc0`.
    """

    localizedIssuerName: Optional[LocalizedString] = None
    """
    Translated strings for the issuerName. Recommended maximum length is 20
    characters to ensure full string is displayed on smaller screens.
    """

    multipleDevicesAndHoldersAllowedStatus: (
        MultipleDevicesAndHoldersAllowedStatus
    ) = MultipleDevicesAndHoldersAllowedStatus.STATUS_UNSPECIFIED
    """
    Identifies whether multiple users and devices will save the same object
    referencing this class.
    """

    callbackOptions: Optional[CallbackOptions] = None
    """
    Callback options to be used to call the issuer back for every save/delete
    of an object for this class by the end-user. All objects of this class are
    eligible for the callback.
    """

    securityAnimation: Optional[SecurityAnimation] = None
    """
    Optional information about the security animation. If this is set a
    security animation will be rendered on pass details.
    """

    viewUnlockRequirement: ViewUnlockRequirement = (
        ViewUnlockRequirement.VIEW_UNLOCK_REQUIREMENT_UNSPECIFIED
    )
    """
    View Unlock Requirement options for the event ticket.
    """

    wideLogo: Optional[Image] = None
    """
    The wide logo of the ticket. When provided, this will be used in place of
    the logo in the top left of the card view.
    """

    notifyPreference: NotificationSettingsForUpdates = (
        NotificationSettingsForUpdates.NOTIFICATION_SETTINGS_FOR_UPDATES_UNSPECIFIED
    )
    """
    Whether or not field updates to this class should trigger notifications.
    When set to NOTIFY, we will attempt to trigger a field update notification
    to users. These notifications will only be sent to users if the field is
    part of an allowlist. If not specified, no notification will be triggered.
    This setting is ephemeral and needs to be set with each PATCH or UPDATE
    request, otherwise a notification will not be triggered.
    """

    appLinkData: Optional[AppLinkData] = None
    """
    Optional app or website link that will be displayed as a button on the
    front of the pass. If AppLinkData is provided for the corresponding object
    that will be used instead.
    """

    valueAddedModuleData: list[ValueAddedModuleData] = Field(
        default_factory=list,
    )
    """
    Optional value added module data. Maximum of ten on the class. For a pass
    only ten will be displayed, prioritizing those from the object.
    """

    merchantLocations: list[MerchantLocation] = Field(
        default_factory=list,
    )
    """
    Merchant locations. There is a maximum of ten on the class. Any additional
    MerchantLocations added beyond the 10 will be rejected. These locations
    will trigger a notification when a user enters within a Google-set radius
    of the point. This field replaces the deprecated LatLongPoints.
    """
