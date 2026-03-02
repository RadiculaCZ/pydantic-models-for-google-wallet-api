# https://developers.google.com/wallet/reference/rest/v1/genericobject

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from .app_link_data import AppLinkData
from .barcode import Barcode
from .grouping_info import GroupingInfo
from .image import Image
from .image_module_data import ImageModuleData
from .links_module_data import LinksModuleData
from .localized_string import LocalizedString
from .merchant_location import MerchantLocation
from .message import Message
from .pass_constraints import PassConstraints
from .rotating_barcode import RotatingBarcode
from .save_restrictions import SaveRestrictions
from .state import State
from .text_module_data import TextModuleData
from .time_interval import TimeInterval
from .value_added_module_data import ValueAddedModuleData


class GenericType(str, Enum):
    """
    The type of the generic card.
    """

    GENERIC_TYPE_UNSPECIFIED = "GENERIC_TYPE_UNSPECIFIED"
    """
    Unspecified generic type.
    """

    GENERIC_SEASON_PASS = "GENERIC_SEASON_PASS"
    """
    Season pass
    """

    GENERIC_UTILITY_BILLS = "GENERIC_UTILITY_BILLS"
    """
    Utility bills
    """

    GENERIC_PARKING_PASS = "GENERIC_PARKING_PASS"
    """
    Parking pass
    """

    GENERIC_VOUCHER = "GENERIC_VOUCHER"
    """
    Voucher
    """

    GENERIC_GYM_MEMBERSHIP = "GENERIC_GYM_MEMBERSHIP"
    """
    Gym membership cards
    """

    GENERIC_LIBRARY_MEMBERSHIP = "GENERIC_LIBRARY_MEMBERSHIP"
    """
    Library membership cards
    """

    GENERIC_RESERVATIONS = "GENERIC_RESERVATIONS"
    """
    Reservations
    """

    GENERIC_AUTO_INSURANCE = "GENERIC_AUTO_INSURANCE"
    """
    Auto-insurance cards
    """

    GENERIC_HOME_INSURANCE = "GENERIC_HOME_INSURANCE"
    """
    Home-insurance cards
    """

    GENERIC_ENTRY_TICKET = "GENERIC_ENTRY_TICKET"
    """
    Entry tickets
    """

    GENERIC_RECEIPT = "GENERIC_RECEIPT"
    """
    Receipts
    """

    GENERIC_LOYALTY_CARD = "GENERIC_LOYALTY_CARD"
    """
    Loyalty cards. Please note that it is advisable to use a dedicated Loyalty
    card pass type instead of this generic type. A dedicated loyalty card pass
    type offers more features and functionality than a generic pass type.
    """

    GENERIC_OTHER = "GENERIC_OTHER"
    """
    Other type
    """


class ExpiryNotification(BaseModel):
    """
    Indicates that the issuer would like Google Wallet to send expiry
    notifications 2 days prior to the card expiration.
    """

    enableNotification: bool = False
    """
    Indicates if the object needs to have expiry notification enabled.
    """


class UpcomingNotification(BaseModel):
    """
    Indicates that the issuer would like Google Wallet to send an upcoming card
    validity notification 1 day before card becomes valid/usable.
    """

    enableNotification: bool = False
    """
    Indicates if the object needs to have upcoming notification enabled.
    """


class Notifications(BaseModel):
    """
    Indicates if the object needs to have notification enabled. We support only
    one of ExpiryNotification/UpcomingNotification. `expiryNotification` takes
    precedence over `upcomingNotification`. In other words if
    `expiryNotification` is set, we ignore the `upcomingNotification` field.
    """

    expiryNotification: Optional[ExpiryNotification] = None
    """
    A notification would be triggered at a specific time before the card
    expires.
    """

    upcomingNotification: Optional[UpcomingNotification] = None
    """
    A notification would be triggered at a specific time before the card
    becomes usable.
    """


class GenericObject(BaseModel):
    """
    Generic Object
    """

    genericType: GenericType
    """
    Specify which GenericType the card belongs to.
    """

    cardTitle: LocalizedString
    """
    Required. The header of the pass. This is usually the Business name such as
    "XXX Gym", "AAA Insurance". This field is required and appears in the
    header row at the very top of the pass.
    """

    subheader: Optional[LocalizedString] = None
    """
    The title label of the pass, such as location where this pass can be used.
    Appears right above the title in the title row in the pass detail view.
    """

    header: LocalizedString
    """
    Required. The title of the pass, such as "50% off coupon" or "Library card"
    or "Voucher". This field is required and appears in the title row of the
    pass detail view.
    """

    logo: Optional[Image] = None
    """
    The logo image of the pass. This image is displayed in the card detail view
    in upper left, and also on the list/thumbnail view. If the logo is not
    present, the first letter of `cardTitle` would be shown as logo.
    """

    hexBackgroundColor: Optional[str] = None
    """
    The background color for the card. If not set, the dominant color of the
    hero image is used, and if no hero image is set, the dominant color of the
    logo is used and if logo is not set, a color would be chosen by Google.
    """

    notifications: Optional[Notifications] = None
    """
    The notification settings that are enabled for this object.
    """

    id: str
    """
    Required. The unique identifier for an object. This ID must be unique
    across all objects from an issuer. This value needs to follow the format
    `issuerID.identifier` where `issuerID` is issued by Google and `identifier`
    is chosen by you. The unique identifier can only include alphanumeric
    characters, `.`, `_`, or `-`.
    """

    classId: str
    """
    Required. The class associated with this object. The class must be of the
    same type as this object, must already exist, and must be approved.

    Class IDs should follow the format `issuerID.identifier` where `issuerID`
    is issued by Google and `identifier` is chosen by you.
    """

    barcode: Optional[Barcode] = None
    """
    The barcode type and value. If pass does not have a barcode, we can allow
    the issuer to set Barcode.alternate_text and display just that.
    """

    heroImage: Optional[Image] = None
    """
    Banner image displayed on the front of the card if present. The image will
    be displayed at 100% width.
    """

    validTimeInterval: Optional[TimeInterval] = None
    """
    The time period this object will be considered valid or usable. When the
    time period is passed, the object will be considered expired, which will
    affect the rendering on user's devices.
    """

    imageModulesData: list[ImageModuleData] = Field(default_factory=list)
    """
    Image module data. Only one of the image from class and one from object
    level will be rendered when both set.
    """

    textModulesData: list[TextModuleData] = Field(default_factory=list)
    """
    Text module data. If `textModulesData` is also defined on the class, both
    will be displayed. The maximum number of these fields displayed is 10 from
    class and 10 from object.
    """

    linksModuleData: Optional[LinksModuleData] = None
    """
    Links module data. If linksModuleData is also defined on the class, both
    will be displayed. The maximum number of these fields displayed is 10 from
    class and 10 from object.
    """

    appLinkData: Optional[AppLinkData] = None
    """
    Optional app or website link that will be displayed as a button on the
    front of the pass. If AppLinkData is provided for the corresponding class
    only object AppLinkData will be displayed.
    """

    groupingInfo: Optional[GroupingInfo] = None
    """
    Information that controls how passes are grouped together.
    """

    smartTapRedemptionValue: Optional[str] = None
    """
    The value that will be transmitted to a Smart Tap certified terminal over
    NFC for this object. The class level fields `enableSmartTap` and
    `redemptionIssuers` must also be set up correctly in order for the pass to
    support Smart Tap. Only ASCII characters are supported.
    """

    rotatingBarcode: Optional[RotatingBarcode] = None
    """
    The rotating barcode settings/details.
    """

    state: State = State.STATE_UNSPECIFIED
    """
    The state of the object. This field is used to determine how an object is
    displayed in the app. For example, an `inactive` object is moved to the
    "Expired passes" section. If this is not provided, the object would be
    considered `ACTIVE`.
    """

    hasUsers: Optional[bool] = None
    """
    Indicates if the object has users. This field is set by the platform.
    """

    messages: list[Message] = Field(default_factory=list)
    """
    An array of messages displayed in the app. All users of this object will
    receive its associated messages. The maximum number of these fields is 10.
    """

    passConstraints: Optional[PassConstraints] = None
    """
    Pass constraints for the object. Includes limiting NFC and screenshot
    behaviors.
    """

    wideLogo: Optional[Image] = None
    """
    The wide logo of the pass. When provided, this will be used in place of the
    logo in the top left of the card view.
    """

    saveRestrictions: Optional[SaveRestrictions] = None
    """
    Restrictions on the object that needs to be verified before the user tries
    to save the pass. Note that this restrictions will only be applied during
    save time. If the restrictions changed after a user saves the pass, the new
    restrictions will not be applied to an already saved pass.
    """

    valueAddedModuleData: list[ValueAddedModuleData] = Field(
        default_factory=list,
        max_length=10,
    )
    """
    Optional value added module data. Maximum of ten on the object.
    """

    linkedObjectIds: list[str] = Field(default_factory=list)
    """
    linkedObjectIds are a list of other objects such as event ticket, loyalty,
    offer, generic, giftcard, transit and boarding pass that should be
    automatically attached to this generic object. If a user had saved this
    generic card, then these linkedObjectIds would be automatically pushed to
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

    merchantLocations: list[MerchantLocation] = Field(default_factory=list)
    """
    Merchant locations. There is a maximum of ten on the object. Any additional
    MerchantLocations added beyond the 10 will be rejected. These locations
    will trigger a notification when a user enters within a Google-set radius
    of the point. This field replaces the deprecated LatLongPoints.
    """
