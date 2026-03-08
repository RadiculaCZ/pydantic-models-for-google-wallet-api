# https://developers.google.com/wallet/reference/rest/v1/flightobject

from enum import Enum
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field
from typing_extensions import deprecated

from .app_link_data import AppLinkData
from .barcode import Barcode
from .flight_class import FlightClass
from .grouping_info import GroupingInfo
from .image import Image
from .image_module_data import ImageModuleData
from .info_module_data import InfoModuleData
from .lat_long_point import LatLongPoint
from .links_module_data import LinksModuleData
from .localized_string import LocalizedString
from .merchant_location import MerchantLocation
from .message import Message
from .notification_settings_for_updates import NotificationSettingsForUpdates
from .pass_constraints import PassConstraints
from .rotating_barcode import RotatingBarcode
from .save_restrictions import SaveRestrictions
from .state import State
from .text_module_data import TextModuleData
from .time_interval import TimeInterval
from .value_added_module_data import ValueAddedModuleData


class BoardingDoor(str, Enum):
    BOARDING_DOOR_UNSPECIFIED = "BOARDING_DOOR_UNSPECIFIED"

    FRONT = "FRONT"

    front = "front"
    """
    Legacy alias for `FRONT`. Deprecated.
    """

    BACK = "BACK"

    back = "back"
    """
    Legacy alias for `BACK`. Deprecated.
    """


class BoardingAndSeatingInfo(BaseModel):
    kind: Annotated[
        Literal["walletobjects#boardingAndSeatingInfo"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#boardingAndSeatingInfo"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#boardingAndSeatingInfo"`.
    """

    boardingGroup: Optional[str] = None
    """
    The value of boarding group (or zone) this passenger shall board with.

    eg: "B"

    The label for this value will be determined by the `boardingPolicy` field
    in the `flightClass` referenced by this object.
    """

    seatNumber: Optional[str] = None
    """
    The value of passenger seat. If there is no specific identifier, use
    `seatAssignment` instead.

    eg: "25A"
    """

    seatClass: Optional[str] = None
    """
    The value of the seat class.

    eg: "Economy" or "Economy Plus"
    """

    boardingPrivilegeImage: Optional[Image] = None
    """
    A small image shown above the boarding barcode. Airlines can use it to
    communicate any special boarding privileges. In the event the security
    program logo is also set, this image might be rendered alongside the logo
    for that security program.
    """

    boardingPosition: Optional[str] = None
    """
    The value of boarding position.

    eg: "76"
    """

    sequenceNumber: Optional[str] = None
    """
    The sequence number on the boarding pass. This usually matches the sequence
    in which the passengers checked in. Airline might use the number for manual
    boarding and bag tags.

    eg: "49"
    """

    boardingDoor: BoardingDoor
    """
    Set this field only if this flight boards through more than one door or
    bridge and you want to explicitly print the door location on the boarding
    pass. Most airlines route their passengers to the right door or bridge by
    refering to doors/bridges by the `seatClass`. In those cases `boardingDoor`
    should not be set.
    """

    seatAssignment: Optional[LocalizedString] = None
    """
    The passenger's seat assignment. To be used when there is no specific
    identifier to use in `seatNumber`.

    eg: "assigned at gate"
    """


class FrequentFlyerInfo(BaseModel):
    kind: Annotated[
        Literal["walletobjects#frequentFlyerInfo"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#frequentFlyerInfo"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#frequentFlyerInfo"`.
    """

    frequentFlyerProgramName: Optional[LocalizedString] = None
    """
    Frequent flyer program name. eg: "Lufthansa Miles & More"
    """

    frequentFlyerNumber: Optional[str] = None
    """
    Frequent flyer number.

    Required for each nested object of kind `walletobjects#frequentFlyerInfo`.
    """


class ReservationInfo(BaseModel):
    kind: Annotated[
        Literal["walletobjects#reservationInfo"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#reservationInfo"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#reservationInfo"`.
    """

    confirmationCode: Optional[str] = None
    """
    Confirmation code needed to check into this flight.

    This is the number that the passenger would enter into a kiosk at the
    airport to look up the flight and print a boarding pass.
    """

    eticketNumber: Optional[str] = None
    """
    E-ticket number.
    """

    frequentFlyerInfo: Optional[FrequentFlyerInfo] = None
    """
    Frequent flyer membership information.
    """


class FlightObject(BaseModel):
    kind: Annotated[
        Literal["walletobjects#flightObject"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#flightObject"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#flightObject"`.
    """

    classReference: Optional[FlightClass] = None
    """
    A copy of the inherited fields of the parent class. These fields are
    retrieved during a GET.
    """

    passengerName: Optional[str] = None
    """
    Required. Passenger name as it would appear on the boarding pass.

    eg: "Dave M Gahan" or "Gahan/Dave" or "GAHAN/DAVEM"
    """

    boardingAndSeatingInfo: Optional[BoardingAndSeatingInfo] = None
    """
    Passenger specific information about boarding and seating.
    """

    reservationInfo: ReservationInfo
    """
    Required. Information about flight reservation.
    """

    securityProgramLogo: Optional[Image] = None
    """
    An image for the security program that applies to the passenger.
    """

    hexBackgroundColor: Optional[str] = None
    """
    The background color for the card. If not set the dominant color of the
    hero image is used, and if no hero image is set, the dominant color of the
    logo is used. The format is `#rrggbb` where `rrggbb` is a hex RGB triplet,
    such as `#ffcc00`. You can also use the shorthand version of the RGB
    triplet which is `#rgb`, such as `#fc0`.
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

    state: State = State.STATE_UNSPECIFIED
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
        list[LatLongPoint],
        deprecated("This field is deprecated!"),
    ] = Field(default_factory=list)
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

    Currently, this can only be set for Flights.
    """

    infoModuleData: Annotated[
        Optional[InfoModuleData],
        deprecated("This field is deprecated!"),
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

    rotatingBarcode: Optional[RotatingBarcode] = None
    """
    The rotating barcode type and value.
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
    automatically attached to this flight object. If a user had saved this
    boarding pass, then these linkedObjectIds would be automatically pushed to
    the user's wallet (unless they turned off the setting to receive such
    linked passes).

    Make sure that objects present in linkedObjectIds are already inserted - if
    not, calls would fail. Once linked, the linked objects cannot be unlinked.
    You cannot link objects belonging to another issuer. There is a limit to
    the number of objects that can be linked to a single object. After the
    limit is reached, new linked objects in the call will be ignored silently.

    Object IDs should follow the format issuer ID.identifier where the former
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
    )
    """
    Optional value added module data. Maximum of ten on the object.
    """

    merchantLocations: list[MerchantLocation] = Field(default_factory=list)
    """
    Merchant locations. There is a maximum of ten on the object. Any additional
    MerchantLocations added beyond the 10 will be rejected. These locations
    will trigger a notification when a user enters within a Google-set radius
    of the point. This field replaces the deprecated LatLongPoints.
    """
