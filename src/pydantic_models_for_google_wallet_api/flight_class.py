# https://developers.google.com/wallet/reference/rest/v1/flightclass

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


class FlightCarrier(BaseModel):
    kind: Annotated[
        Literal["walletobjects#flightCarrier"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#flightCarrier"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#flightCarrier"`.
    """

    carrierIataCode: Optional[str] = Field(
        None,
        min_length=2,
        max_length=2,
        pattern=r"^[A-Z]{2}$",
    )
    """
    Two character IATA airline code of the marketing carrier (as opposed to
    operating carrier). Exactly one of this or `carrierIcaoCode` needs to be
    provided for `carrier` and `operatingCarrier`.

    eg: "LX" for Swiss Air
    """

    carrierIcaoCode: Optional[str] = Field(
        None,
        min_length=3,
        max_length=3,
        pattern=r"^[A-Z]{3}$",
    )
    """
    Three character ICAO airline code of the marketing carrier (as opposed to
    operating carrier). Exactly one of this or `carrierIataCode` needs to be
    provided for `carrier` and `operatingCarrier`.

    eg: "EZY" for Easy Jet
    """

    airlineName: Optional[LocalizedString] = None
    """
    A localized name of the airline specified by carrierIataCode. If unset,
    `issuerName` or `localizedIssuerName` from `FlightClass` will be used for
    display purposes.

    eg: "Swiss Air" for "LX"
    """

    airlineLogo: Optional[Image] = None
    """
    A logo for the airline described by carrierIataCode and
    localizedAirlineName. This logo will be rendered at the top of the detailed
    card view.
    """

    airlineAllianceLogo: Optional[Image] = None
    """
    A logo for the airline alliance, displayed below the QR code that the
    passenger scans to board.
    """

    wideAirlineLogo: Optional[Image] = None
    """
    The wide logo of the airline. When provided, this will be used in place of
    the airline logo in the top left of the card view.
    """


class FlightHeader(BaseModel):
    kind: Annotated[
        Literal["walletobjects#flightHeader"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#flightHeader"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#flightHeader"`.
    """

    carrier: FlightCarrier
    """
    Information about airline carrier. This is a required property of
    `flightHeader`.
    """

    flightNumber: str
    """
    The flight number without IATA carrier code. This field should contain only
    digits. This is a required property of `flightHeader`.

    eg: "123"
    """

    operatingCarrier: Optional[FlightCarrier] = None
    """
    Information about operating airline carrier.
    """

    operatingFlightNumber: Optional[str] = None
    """
    The flight number used by the operating carrier without IATA carrier code.
    This field should contain only digits.

    eg: "234"
    """

    flightNumberDisplayOverride: Optional[str] = None
    """
    Override value to use for flight number. The default value used for display
    purposes is carrier + flightNumber. If a different value needs to be shown
    to passengers, use this field to override the default behavior.

    eg: "XX1234 / YY576"
    """


class AirportInfo(BaseModel):
    kind: Annotated[
        Literal["walletobjects#airportInfo"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#airportInfo"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#airportInfo"`.
    """

    airportIataCode: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern=r"^[A-Z]{3}$",
    )
    """
    Three character IATA airport code. This is a required field for `origin`
    and `destination`.

    eg: "SFO"
    """

    terminal: Optional[str] = None
    """
    Terminal name. Eg: "INTL" or "I"
    """

    gate: Optional[str] = None
    """
    A name of the gate. Eg: "B59" or "59"
    """

    airportNameOverride: Optional[LocalizedString] = None
    """
    Optional field that overrides the airport city name defined by IATA. By
    default, Google takes the `airportIataCode` provided and maps it to the
    official airport city name defined by IATA.

    Official IATA airport city names can be found at
    [IATA airport city names](http://www.iata.org/publications/Pages/code-search.aspx)
    website. For example, for the airport IATA code "LTN", IATA website tells
    us that the corresponding airport city is "London".

    If this field is not populated, Google would display "London".

    However, populating this field with a custom name (eg: "London Luton")
    would override it.
    """


class FlightStatus(str, Enum):
    FLIGHT_STATUS_UNSPECIFIED = "FLIGHT_STATUS_UNSPECIFIED"

    SCHEDULED = "SCHEDULED"
    """
    Flight is on time, early, or delayed.
    """

    scheduled = "scheduled"
    """
    Legacy alias for `SCHEDULED`. Deprecated.
    """

    ACTIVE = "ACTIVE"
    """
    Flight is in progress (taxiing, taking off, landing, airborne).
    """

    active = "active"
    """
    Legacy alias for `ACTIVE`. Deprecated.
    """

    LANDED = "LANDED"
    """
    Flight landed at the original destination.
    """

    landed = "landed"
    """
    Legacy alias for `LANDED`. Deprecated.
    """

    CANCELLED = "CANCELLED"
    """
    Flight is cancelled.
    """

    cancelled = "cancelled"
    """
    Legacy alias for `CANCELLED`. Deprecated.
    """

    REDIRECTED = "REDIRECTED"
    """
    Flight is airborne but heading to a different airport than the original
    destination.
    """

    redirected = "redirected"
    """
    Legacy alias for `REDIRECTED`. Deprecated.
    """

    DIVERTED = "DIVERTED"
    """
    Flight has already landed at a different airport than the original
    destination.
    """

    diverted = "diverted"
    """
    Legacy alias for `DIVERTED`. Deprecated.
    """


class BoardingPolicy(str, Enum):
    BOARDING_POLICY_UNSPECIFIED = "BOARDING_POLICY_UNSPECIFIED"

    ZONE_BASED = "ZONE_BASED"

    zoneBased = "zoneBased"
    """
    Legacy alias for `ZONE_BASED`. Deprecated.
    """

    GROUP_BASED = "GROUP_BASED"

    groupBased = "groupBased"
    """
    Legacy alias for `GROUP_BASED`. Deprecated.
    """

    BOARDING_POLICY_OTHER = "BOARDING_POLICY_OTHER"

    boardingPolicyOther = "boardingPolicyOther"
    """
    Legacy alias for `BOARDING_POLICY_OTHER`. Deprecated.
    """


class SeatClassPolicy(str, Enum):
    SEAT_CLASS_POLICY_UNSPECIFIED = "SEAT_CLASS_POLICY_UNSPECIFIED"

    CABIN_BASED = "CABIN_BASED"

    cabinBased = "cabinBased"
    """
    Legacy alias for `CABIN_BASED`. Deprecated.
    """

    CLASS_BASED = "CLASS_BASED"

    classBased = "classBased"
    """
    Legacy alias for `CLASS_BASED`. Deprecated.
    """

    TIER_BASED = "TIER_BASED"

    tierBased = "tierBased"
    """
    Legacy alias for `TIER_BASED`. Deprecated.
    """

    SEAT_CLASS_POLICY_OTHER = "SEAT_CLASS_POLICY_OTHER"

    seatClassPolicyOther = "seatClassPolicyOther"
    """
    Legacy alias for `SEAT_CLASS_POLICY_OTHER`. Deprecated.
    """


class BoardingAndSeatingPolicy(BaseModel):
    kind: Annotated[
        Literal["walletobjects#boardingAndSeatingPolicy"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#boardingAndSeatingPolicy"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#boardingAndSeatingPolicy"`.
    """

    boardingPolicy: BoardingPolicy
    """
    Indicates the policy the airline uses for boarding. If unset, Google will
    default to `zoneBased`.
    """

    seatClassPolicy: SeatClassPolicy
    """
    Seating policy which dictates how we display the seat class. If unset,
    Google will default to `cabinBased`.
    """


class FlightClass(BaseModel):
    kind: Annotated[
        Literal["walletobjects#flightClass"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#flightClass"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#flightClass"`.
    """

    localScheduledDepartureDateTime: str
    """
    Required. The scheduled date and time when the aircraft is expected to
    depart the gate (not the runway)

    Note: This field should not change too close to the departure time. For
    updates to departure times (delays, etc), please set
    `localEstimatedOrActualDepartureDateTime`.

    This is an ISO 8601 extended format date/time without an offset. Time may
    be specified up to millisecond precision.

    eg: `2027-03-05T06:30:00`

    This should be the local date/time at the airport (not a UTC time).

    Google will reject the request if UTC offset is provided. Time zones will
    be calculated by Google based on departure airport.
    """

    localEstimatedOrActualDepartureDateTime: Optional[str] = None
    """
    The estimated time the aircraft plans to pull from the gate or the actual
    time the aircraft already pulled from the gate. Note: This is not the
    runway time.

    This field should be set if at least one of the below is true:
    - It differs from the scheduled time. Google will use it to calculate the
      delay.
    - The aircraft already pulled from the gate. Google will use it to inform
      the user when the flight actually departed.
    
    This is an ISO 8601 extended format date/time without an offset. Time may
    be specified up to millisecond precision.

    eg: `2027-03-05T06:30:00`

    This should be the local date/time at the airport (not a UTC time).

    Google will reject the request if UTC offset is provided. Time zones will
    be calculated by Google based on departure airport.
    """

    localBoardingDateTime: Optional[str] = None
    """
    The boarding time as it would be printed on the boarding pass.

    This is an ISO 8601 extended format date/time without an offset. Time may
    be specified up to millisecond precision.

    eg: `2027-03-05T06:30:00`

    This should be the local date/time at the airport (not a UTC time).

    Google will reject the request if UTC offset is provided. Time zones will
    be calculated by Google based on departure airport.
    """

    localScheduledArrivalDateTime: Optional[str] = None
    """
    The scheduled time the aircraft plans to reach the destination gate (not
    the runway).

    Note: This field should not change too close to the flight time. For
    updates to departure times (delays, etc), please set
    `localEstimatedOrActualArrivalDateTime`.

    This is an ISO 8601 extended format date/time without an offset. Time may
    be specified up to millisecond precision.

    eg: `2027-03-05T06:30:00`

    This should be the local date/time at the airport (not a UTC time).

    Google will reject the request if UTC offset is provided. Time zones will
    be calculated by Google based on arrival airport.
    """

    localEstimatedOrActualArrivalDateTime: Optional[str] = None
    """
    The estimated time the aircraft plans to reach the destination gate (not
    the runway) or the actual time it reached the gate.

    This field should be set if at least one of the below is true:
    - It differs from the scheduled time. Google will use it to calculate the
      delay.
    - The aircraft already arrived at the gate. Google will use it to inform
      the user that the flight has arrived at the gate.

    This is an ISO 8601 extended format date/time without an offset. Time may
    be specified up to millisecond precision.

    eg: `2027-03-05T06:30:00`

    This should be the local date/time at the airport (not a UTC time).

    Google will reject the request if UTC offset is provided. Time zones will
    be calculated by Google based on arrival airport.
    """

    flightHeader: FlightHeader
    """
    Required. Information about the flight carrier and number.
    """

    origin: AirportInfo
    """
    Required. Origin airport.
    """

    destination: AirportInfo
    """
    Required. Destination airport.
    """

    flightStatus: FlightStatus = FlightStatus.FLIGHT_STATUS_UNSPECIFIED
    """
    Status of this flight.

    If unset, Google will compute status based on data from other sources, such
    as FlightStats, etc.

    Note: Google-computed status will not be returned in API responses.
    """

    boardingAndSeatingPolicy: Optional[BoardingAndSeatingPolicy] = None
    """
    Policies for boarding and seating. These will inform which labels will be
    shown to users.
    """

    localGateClosingDateTime: Optional[str] = None
    """
    The gate closing time as it would be printed on the boarding pass. Do not
    set this field if you do not want to print it in the boarding pass.

    This is an ISO 8601 extended format date/time without an offset. Time may
    be specified up to millisecond precision.

    eg: `2027-03-05T06:30:00`

    This should be the local date/time at the airport (not a UTC time).

    Google will reject the request if UTC offset is provided. Time zones will
    be calculated by Google based on departure airport.
    """

    classTemplateInfo: Optional[ClassTemplateInfo] = None
    """
    Template information about how the class should be displayed. If unset,
    Google will fallback to a default set of fields to display.
    """

    languageOverride: Optional[str] = Field(
        None,
        min_length=2,
        # See https://en.wikipedia.org/wiki/IETF_language_tag#Syntax_of_language_tags
        pattern=r"^[a-z]{2,3}(-[a-z]{3}){0,3}(-[A-Z][a-z]{3})?(-([A-Z]{2}|\d{3}))?(-([a-z]{5,8}|\d[a-z]{3}))*(-[a-wyz](-[a-z]{2,8})+)*(-x(-[a-z]{1,8})+)?$",
    )
    """
    If this field is present, boarding passes served to a user's device will
    always be in this language. Represents the BCP 47 language tag. Example
    values are "en-US", "en-GB", "de", or "de-AT".
    """

    id: str
    """
    Required. The unique identifier for a class. This ID must be unique across
    all classes from an issuer. This value should follow the format
    `issuer ID.identifier` where the former is issued by Google and latter is
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

    issuerName: str
    """
    Required. The issuer name. Recommended maximum length is 20 characters to
    ensure full string is displayed on smaller screens.
    """

    messages: list[Message] = Field(default_factory=list, max_length=10)
    """
    An array of messages displayed in the app. All users of this object will
    receive its associated messages. The maximum number of these fields is 10.
    """

    allowMultipleUsersPerObject: Annotated[
        Optional[bool],
        deprecated("This item is deprecated!"),
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
        list[LatLongPoint],
        deprecated("This item is deprecated!"),
    ] = Field(default_factory=list)
    """
    Note: This field is currently not supported to trigger geo notifications.
    """

    reviewStatus: ReviewStatus
    """
    Required. The status of the class. This field can be set to `draft` or
    `underReview` using the insert, patch, or update API calls. Once the review
    state is changed from `draft` it may not be changed back to `draft`.

    You should keep this field to `draft` when the class is under development.
    A `draft` class cannot be used to create any object.

    You should set this field to `underReview` when you believe the class is
    ready for use. The platform will automatically set this field to `approved`
    and it can be immediately used to create or migrate objects.

    When updating an already `approved` class you should keep setting this
    field to `underReview`.
    """

    review: Optional[Review] = None
    """
    The review comments set by the platform when a class is marked `approved`
    or `rejected`.
    """

    infoModuleData: Annotated[
        list[InfoModuleData],
        deprecated("This item is deprecated!"),
    ] = Field(default_factory=list)
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
    Links module data. If links module data is also defined on the object, both
    will be displayed.
    """

    redemptionIssuers: list[str] = Field(default_factory=list)
    """
    int64 format

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
    View Unlock Requirement options for the boarding pass.
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
        max_length=10,
    )
    """
    Optional value added module data. Maximum of ten on the class. For a pass
    only ten will be displayed, prioritizing those from the object.
    """

    merchantLocations: list[MerchantLocation] = Field(default_factory=list)
    """
    Merchant locations. There is a maximum of ten on the class. Any additional
    MerchantLocations added beyond the 10 will be rejected by the validator.
    These locations will trigger a notification when a user enters within a
    Google-set radius of the point. This field replaces the deprecated
    LatLongPoints.
    """
