# https://developers.google.com/wallet/reference/rest/v1/transitobject
from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field
from typing_extensions import deprecated

from .app_link_data import AppLinkData
from .barcode import Barcode
from .grouping_info import GroupingInfo
from .image import Image
from .image_module_data import ImageModuleData
from .info_module_data import InfoModuleData
from .lat_long_point import LatLongPoint
from .links_module_data import LinksModuleData
from .localized_string import LocalizedString
from .merchant_location import MerchantLocation
from .message import Message
from .money import Money
from .notification_settings_for_updates import NotificationSettingsForUpdates
from .pass_constraints import PassConstraints
from .rotating_barcode import RotatingBarcode
from .save_restrictions import SaveRestrictions
from .state import State as ObjectState
from .text_module_data import TextModuleData
from .time_interval import TimeInterval
from .transit_class import TransitClass
from .value_added_module_data import ValueAddedModuleData


class PassengerType(str, Enum):
    PASSENGER_TYPE_UNSPECIFIED = "PASSENGER_TYPE_UNSPECIFIED"

    SINGLE_PASSENGER = "SINGLE_PASSENGER"

    singlePassenger = "singlePassenger"
    """
    Legacy alias for `SINGLE_PASSENGER`. Deprecated.
    """

    MULTIPLE_PASSENGERS = "MULTIPLE_PASSENGERS"

    multiplePassengers = "multiplePassengers"
    """
    Legacy alias for `MULTIPLE_PASSENGERS`. Deprecated.
    """


class TicketStatus(str, Enum):
    TICKET_STATUS_UNSPECIFIED = "TICKET_STATUS_UNSPECIFIED"

    USED = "USED"

    used = "used"
    """
    Legacy alias for `USED`. Deprecated.
    """

    REFUNDED = "REFUNDED"

    refunded = "refunded"
    """
    Legacy alias for `REFUNDED`. Deprecated.
    """

    EXCHANGED = "EXCHANGED"

    exchanged = "exchanged"
    """
    Legacy alias for `EXCHANGED`. Deprecated.
    """


class ConcessionCategory(str, Enum):
    CONCESSION_CATEGORY_UNSPECIFIED = "CONCESSION_CATEGORY_UNSPECIFIED"

    ADULT = "ADULT"

    adult = "adult"
    """
    Legacy alias for `ADULT`. Deprecated.
    """

    CHILD = "CHILD"

    child = "child"
    """
    Legacy alias for `CHILD`. Deprecated.
    """

    SENIOR = "SENIOR"

    senior = "senior"
    """
    Legacy alias for `SENIOR`. Deprecated.
    """


class TicketRestrictions(BaseModel):
    routeRestrictions: Optional[LocalizedString] = None
    """
    Restrictions about routes that may be taken. For example, this may be the
    string "Reserved CrossCountry trains only".
    """

    routeRestrictionsDetails: Optional[LocalizedString] = None
    """
    More details about the above `routeRestrictions`.
    """

    timeRestrictions: Optional[LocalizedString] = None
    """
    Restrictions about times this ticket may be used.
    """

    otherRestrictions: Optional[LocalizedString] = None
    """
    Extra restrictions that don't fall under the "route" or "time" categories.
    """


class TicketCost(BaseModel):
    faceValue: Optional[Money] = None
    """
    The face value of the ticket.
    """

    purchasePrice: Optional[Money] = None
    """
    The actual purchase price of the ticket, after tax and/or discounts.
    """

    discountMessage: Optional[LocalizedString] = None
    """
    A message describing any kind of discount that was applied.
    """


class PurchaseDetails(BaseModel):
    purchaseReceiptNumber: Optional[str] = None
    """
    Receipt number/identifier for tracking the ticket purchase via the body
    that sold the ticket.
    """

    purchaseDateTime: Optional[str] = None
    """
    The purchase date/time of the ticket.

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

    Without offset information, some rich features may not be available.
    """

    accountId: Optional[str] = None
    """
    ID of the account used to purchase the ticket.
    """

    confirmationCode: Optional[str] = None
    """
    The confirmation code for the purchase. This may be the same for multiple
    different tickets and is used to group tickets together.
    """

    ticketCost: Optional[TicketCost] = None
    """
    The cost of the ticket.
    """


class FareClass(str, Enum):
    FARE_CLASS_UNSPECIFIED = "FARE_CLASS_UNSPECIFIED"

    ECONOMY = "ECONOMY"

    economy = "economy"
    """
    Legacy alias for `ECONOMY`. Deprecated.
    """

    FIRST = "FIRST"

    first = "first"
    """
    Legacy alias for `FIRST`. Deprecated.
    """

    BUSINESS = "BUSINESS"

    business = "business"
    """
    Legacy alias for `BUSINESS`. Deprecated.
    """


class TicketSeat(BaseModel):
    fareClass: FareClass = FareClass.FARE_CLASS_UNSPECIFIED
    """
    The fare class of the ticketed seat.
    """

    customFareClass: Optional[LocalizedString] = None
    """
    A custom fare class to be used if no `fareClass` applies. Both `fareClass`
    and `customFareClass` may not be set.
    """

    coach: Optional[str] = None
    """
    The identifier of the train car or coach in which the ticketed seat is
    located. Eg. "10"
    """

    seat: Optional[str] = None
    """
    The identifier of where the ticketed seat is located. Eg. "42". If there is
    no specific identifier, use `seatAssignment` instead.
    """

    seatAssignment: Optional[LocalizedString] = None
    """
    The passenger's seat assignment. Eg. "no specific seat". To be used when
    there is no specific identifier to use in `seat`.
    """


class TripType(str, Enum):
    TRIP_TYPE_UNSPECIFIED = "TRIP_TYPE_UNSPECIFIED"

    ROUND_TRIP = "ROUND_TRIP"

    roundTrip = "roundTrip"
    """
    Legacy alias for `ROUND_TRIP`. Deprecated.
    """

    ONE_WAY = "ONE_WAY"

    oneWay = "oneWay"
    """
    Legacy alias for `ONE_WAY`. Deprecated.
    """


class State(str, Enum):
    UNKNOWN_STATE = "UNKNOWN_STATE"

    NOT_ACTIVATED = "NOT_ACTIVATED"
    """
    Not-Activated, this is the default status
    """

    not_activated = "not_activated"
    """
    Legacy alias for `NOT_ACTIVATED`. Deprecated.
    """

    ACTIVATED = "ACTIVATED"
    """
    Activated
    """

    activated = "activated"
    """
    Legacy alias for `ACTIVATED`. Deprecated.
    """


class ActivationStatus(BaseModel):
    state: State = State.UNKNOWN_STATE


class DeviceContext(BaseModel):
    deviceToken: Optional[str] = None
    """
    If set, redemption information will only be returned to the given device
    upon activation of the object. This should not be used as a stable
    identifier to trace a user's device. It can change across different passes
    for the same device or even across different activations for the same
    device. When setting this, callers must also set hasLinkedDevice on the
    object being activated.
    """


class TicketLeg(BaseModel):
    originStationCode: Optional[str] = None
    """
    The origin station code. This is required if `destinationStationCode` is
    present or if `originName` is not present.
    """

    originName: Optional[LocalizedString] = None
    """
    The name of the origin station. This is required if `destinationName` is
    present or if `originStationCode` is not present.
    """

    destinationStationCode: Optional[str] = None
    """
    The destination station code.
    """

    destinationName: Optional[LocalizedString] = None
    """
    The destination name.
    """

    departureDateTime: Optional[str] = None
    """
    The date/time of departure. This is required if there is no validity time
    interval set on the transit object.

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
    date/time". This should be the local date/time at the origin station. For
    example, if the departure occurs at the 20th hour of June 5th, 2018 at the
    origin station, the local date/time portion should be
    `2018-06-05T20:00:00`. If the local date/time at the origin station is 4
    hours before UTC, an offset of `-04:00` may be appended.

    Without offset information, some rich features may not be available.
    """

    arrivalDateTime: Optional[str] = None
    """
    The date/time of arrival.

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
    date/time". This should be the local date/time at the origin station. For
    example, if the departure occurs at the 20th hour of June 5th, 2018 at the
    origin station, the local date/time portion should be
    `2018-06-05T20:00:00`. If the local date/time at the origin station is 4
    hours before UTC, an offset of `-04:00` may be appended.

    Without offset information, some rich features may not be available.
    """

    fareName: Optional[LocalizedString] = None
    """
    Short description/name of the fare for this leg of travel. Eg "Anytime
    Single Use".
    """

    carriage: Optional[str] = None
    """
    The train or ship name/number that the passenger needs to board.
    """

    platform: Optional[str] = None
    """
    The platform or gate where the passenger can board the carriage.
    """

    zone: Optional[str] = None
    """
    The zone of boarding within the platform.
    """

    ticketSeat: Optional[TicketSeat] = None
    """
    The reserved seat for the passenger(s). If more than one seat is to be
    specified then use the `ticketSeats` field instead. Both `ticketSeat` and
    `ticketSeats` may not be set.
    """

    ticketSeats: Optional[list[TicketSeat]] = None
    """
    The reserved seat for the passenger(s). If only one seat is to be specified
    then use the `ticketSeat` field instead. Both `ticketSeat` and
    `ticketSeats` may not be set.
    """

    transitOperatorName: Optional[LocalizedString] = None
    """
    The name of the transit operator that is operating this leg of a trip.
    """

    transitTerminusName: Optional[LocalizedString] = None
    """
    Terminus station or destination of the train/bus/etc.
    """


class TransitObject(BaseModel):
    classReference: Optional[TransitClass] = None
    """
    A copy of the inherited fields of the parent class. These fields are
    retrieved during a GET.
    """

    ticketNumber: Optional[str] = None
    """
    The number of the ticket. This is a unique identifier for the ticket in the
    transit operator's system.
    """

    passengerType: PassengerType = PassengerType.PASSENGER_TYPE_UNSPECIFIED
    """
    The number of passengers.
    """

    passengerNames: Optional[str] = None
    """
    The name(s) of the passengers the ticket is assigned to. The above
    `passengerType` field is meant to give Google context on this field.
    """

    tripId: Optional[str] = None
    """
    This id is used to group tickets together if the user has saved multiple
    tickets for the same trip.
    """

    ticketStatus: TicketStatus = TicketStatus.TICKET_STATUS_UNSPECIFIED
    """
    The status of the ticket. For states which affect display, use the `state`
    field instead.
    """

    customTicketStatus: Optional[LocalizedString] = None
    """
    A custom status to use for the ticket status value when `ticketStatus` does
    not provide the right option. Both `ticketStatus` and `customTicketStatus`
    may not be set.
    """

    concessionCategory: ConcessionCategory = (
        ConcessionCategory.CONCESSION_CATEGORY_UNSPECIFIED
    )
    """
    The concession category for the ticket.
    """

    customConcessionCategory: Optional[LocalizedString] = None
    """
    A custom concession category to use when `concessionCategory` does not
    provide the right option. Both `concessionCategory` and
    `customConcessionCategory` may not be set.
    """

    ticketRestrictions: Optional[TicketRestrictions] = None
    """
    Information about what kind of restrictions there are on using this ticket.
    For example, which days of the week it must be used, or which routes are
    allowed to be taken.
    """

    purchaseDetails: Optional[PurchaseDetails] = None
    """
    Purchase details for this ticket.
    """

    ticketLeg: Optional[TicketLeg] = None
    """
    A single ticket leg contains departure and arrival information along with
    boarding and seating information. If more than one leg is to be specified
    then use the `ticketLegs` field instead. Both `ticketLeg` and `ticketLegs`
    may not be set.
    """

    ticketLegs: Optional[list[TicketLeg]] = None
    """
    Each ticket may contain one or more legs. Each leg contains departure and
    arrival information along with boarding and seating information. If only
    one leg is to be specified then use the `ticketLeg` field instead. Both
    `ticketLeg` and `ticketLegs` may not be set.
    """

    hexBackgroundColor: Optional[str] = None
    """
    The background color for the card. If not set the dominant color of the
    hero image is used, and if no hero image is set, the dominant color of the
    logo is used. The format is `#rrggbb` where `rrggbb` is a hex RGB triplet,
    such as `#ffcc00`. You can also use the shorthand version of the RGB
    triplet which is `#rgb`, such as `#fc0`.
    """

    tripType: TripType = TripType.TRIP_TYPE_UNSPECIFIED
    """
    Required. The type of trip this transit object represents. Used to
    determine the pass title and/or which symbol to use between the origin and
    destination.
    """

    id: str
    """
    Required. The unique identifier for an object. This ID must be unique
    across all objects from an issuer. This value should follow the format
    `issuer ID.identifier` where the former is issued by Google and latter is
    chosen by you. The unique identifier should only include alphanumeric
    characters, '.', '_', or '-'.
    """

    classId: str
    """
    Required. The class associated with this object. The class must be of the
    same type as this object, must already exist, and must be approved.

    Class IDs should follow the format `issuer ID.identifier` where the former
    is issued by Google and latter is chosen by you.
    """

    version: Annotated[
        Optional[str],
        deprecated("This item is deprecated!"),
    ] = None
    """
    int64 format

    Deprecated
    """

    state: ObjectState = ObjectState.STATE_UNSPECIFIED
    """
    Required. The state of the object. This field is used to determine how an
    object is displayed in the app. For example, an `inactive` object is moved
    to the "Expired passes" section.
    """

    barcode: Optional[Barcode] = None
    """
    The barcode type and value.
    """

    messages: list[Message] = Field(default_factory=list, max_length=10)
    """
    An array of messages displayed in the app. All users of this object will
    receive its associated messages. The maximum number of these fields is 10.
    """

    validTimeInterval: Optional[TimeInterval] = None
    """
    The time period this object will be `active` and object can be used. An
    object's state will be changed to `expired` when this time period has
    passed.
    """

    locations: Annotated[
        Optional[list[LatLongPoint]],
        deprecated("This item is deprecated!"),
    ] = None
    """
    Note: This field is currently not supported to trigger geo notifications.
    """

    hasUsers: Optional[bool] = None
    """
    Indicates if the object has users. This field is set by the platform.
    """

    smartTapRedemptionValue: Optional[str] = None
    """
    The value that will be transmitted to a Smart Tap certified terminal over
    NFC for this object. The class level fields `enableSmartTap` and
    `redemptionIssuers` must also be set up correctly in order for the pass to
    support Smart Tap. Only ASCII characters are supported.
    """

    hasLinkedDevice: Optional[bool] = None
    """
    Whether this object is currently linked to a single device. This field is
    set by the platform when a user saves the object, linking it to their
    device. Intended for use by select partners. Contact support for additional
    information.
    """

    disableExpirationNotification: bool = False
    """
    Indicates if notifications should explicitly be suppressed. If this field
    is set to true, regardless of the `messages` field, expiration
    notifications to the user will be suppressed. By default, this field is set
    to false.

    Currently, this can only be set for offers.
    """

    infoModuleData: Annotated[
        Optional[InfoModuleData],
        deprecated("This item is deprecated!"),
    ] = None
    """
    Deprecated. Use textModulesData instead.
    """

    imageModulesData: list[ImageModuleData] = Field(default_factory=list)
    """
    Image module data. The maximum number of these fields displayed is 1 from
    object level and 1 for class object level.
    """

    textModulesData: list[TextModuleData] = Field(default_factory=list)
    """
    Text module data. If text module data is also defined on the class, both
    will be displayed. The maximum number of these fields displayed is 10 from
    the object and 10 from the class.
    """

    linksModuleData: Optional[LinksModuleData] = None
    """
    Links module data. If links module data is also defined on the class, both
    will be displayed.
    """

    appLinkData: Optional[AppLinkData] = None
    """
    Optional app or website link that will be displayed as a button on the
    front of the pass. If AppLinkData is provided for the corresponding class
    only object AppLinkData will be displayed.
    """

    activationStatus: Optional[ActivationStatus] = None
    """
    The activation status for the object. Required if the class has
    `activationOptions` set.
    """

    rotatingBarcode: Optional[RotatingBarcode] = None
    """
    The rotating barcode type and value.
    """

    deviceContext: Optional[DeviceContext] = None
    """
    Device context associated with the object.
    """

    heroImage: Optional[Image] = None
    """
    Optional banner image displayed on the front of the card. If none is
    present, hero image of the class, if present, will be displayed. If hero
    image of the class is also not present, nothing will be displayed.
    """

    groupingInfo: Optional[GroupingInfo] = None
    """
    Information that controls how passes are grouped together.
    """

    passConstraints: Optional[PassConstraints] = None
    """
    Pass constraints for the object. Includes limiting NFC and screenshot
    behaviors.
    """

    saveRestrictions: Optional[SaveRestrictions] = None
    """
    Restrictions on the object that needs to be verified before the user tries
    to save the pass. Note that this restrictions will only be applied during
    save time. If the restrictions changed after a user saves the pass, the new
    restrictions will not be applied to an already saved pass.
    """

    linkedObjectIds: list[str] = Field(default_factory=list)
    """
    linkedObjectIds are a list of other objects such as event ticket, loyalty,
    offer, generic, giftcard, transit and boarding pass that should be
    automatically attached to this transit object. If a user had saved this
    transit card, then these linkedObjectIds would be automatically pushed to
    the user's wallet (unless they turned off the setting to receive such
    linked passes).

    Make sure that objects present in linkedObjectIds are already inserted - if
    not, calls would fail. Once linked, the linked objects cannot be unlinked.
    You cannot link objects belonging to another issuer. There is a limit to
    the number of objects that can be linked to a single object. After the
    limit is reached, new linked objects in the call will be ignored silently.

    Object IDs should follow the format `issuer ID.identifier` where the former
    is issued by Google and the latter is chosen by you.
    """

    notifyPreference: NotificationSettingsForUpdates = (
        NotificationSettingsForUpdates.NOTIFICATION_SETTINGS_FOR_UPDATES_UNSPECIFIED
    )
    """
    Whether or not field updates to this object should trigger notifications.
    When set to NOTIFY, we will attempt to trigger a field update notification
    to users. These notifications will only be sent to users if the field is
    part of an allowlist. If set to DO_NOT_NOTIFY or
    NOTIFICATION_SETTINGS_UNSPECIFIED, no notification will be triggered. This
    setting is ephemeral and needs to be set with each PATCH or UPDATE request,
    otherwise a notification will not be triggered.
    """

    valueAddedModuleData: list[ValueAddedModuleData] = Field(
        default_factory=list,
        max_length=10,
    )
    """
    Optional value added module data. Maximum of ten on the object.
    """

    merchantLocations: list[MerchantLocation] = Field(
        default_factory=list,
        max_length=10,
    )
    """
    Merchant locations. There is a maximum of ten on the object. Any additional
    MerchantLocations added beyond the 10 will be rejected. These locations
    will trigger a notification when a user enters within a Google-set radius
    of the point. This field replaces the deprecated LatLongPoints.
    """
