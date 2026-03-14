# https://developers.google.com/wallet/reference/rest/v1/offerclass

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


class RedemptionChannel(str, Enum):
    REDEMPTION_CHANNEL_UNSPECIFIED = "REDEMPTION_CHANNEL_UNSPECIFIED"

    INSTORE = "INSTORE"

    instore = "instore"
    """
    Legacy alias for `INSTORE`. Deprecated.
    """

    ONLINE = "ONLINE"

    online = "online"
    """
    Legacy alias for `ONLINE`. Deprecated.
    """

    BOTH = "BOTH"

    both = "both"
    """
    Legacy alias for `BOTH`. Deprecated.
    """

    TEMPORARY_PRICE_REDUCTION = "TEMPORARY_PRICE_REDUCTION"

    temporaryPriceReduction = "temporaryPriceReduction"
    """
    Legacy alias for `TEMPORARY_PRICE_REDUCTION`. Deprecated.
    """


class OfferClass(BaseModel):
    kind: Annotated[
        Literal["walletobjects#offerClass"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#offerClass"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#offerClass"`.
    """

    title: str
    """
    Required. The title of the offer, such as "20% off any t-shirt."
    Recommended maximum length is 60 characters to ensure full string is
    displayed on smaller screens.
    """

    redemptionChannel: RedemptionChannel = (
        RedemptionChannel.REDEMPTION_CHANNEL_UNSPECIFIED
    )
    """
    Required. The redemption channels applicable to this offer.
    """

    provider: str
    """
    Required. The offer provider (either the aggregator name or merchant name).
    Recommended maximum length is 12 characters to ensure full string is
    displayed on smaller screens.
    """

    titleImage: Image
    """
    The title image of the offer. This image is displayed in both the details
    and list views of the app.
    """

    details: Optional[str] = None
    """
    The details of the offer.
    """

    finePrint: Optional[str] = None
    """
    The fine print or terms of the offer, such as "20% off any t-shirt at
    Adam's Apparel."
    """

    helpUri: Optional[Uri] = None
    """
    The help link for the offer, such as `http://myownpersonaldomain.com/help`
    """

    localizedTitle: Optional[LocalizedString] = None
    """
    Translated strings for the title. Recommended maximum length is 60
    characters to ensure full string is displayed on smaller screens.
    """

    localizedProvider: Optional[LocalizedString] = None
    """
    Translated strings for the provider. Recommended maximum length is 12
    characters to ensure full string is displayed on smaller screens.
    """

    localizedDetails: Optional[LocalizedString] = None
    """
    Translated strings for the details.
    """

    localizedFinePrint: Optional[LocalizedString] = None
    """
    Translated strings for the finePrint.
    """

    shortTitle: Optional[str] = None
    """
    A shortened version of the title of the offer, such as "20% off," shown to
    users as a quick reference to the offer contents. Recommended maximum
    length is 20 characters.
    """

    localizedShortTitle: Optional[LocalizedString] = None
    """
    Translated strings for the short title. Recommended maximum length is 20
    characters.
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

    reviewStatus: ReviewStatus = ReviewStatus.REVIEW_STATUS_UNSPECIFIED
    """
    Required. The status of the class. This field can be set to `draft` or The
    status of the class. This field can be set to `draft` or `underReview`
    using the insert, patch, or update API calls. Once the review state is
    changed from `draft` it may not be changed back to `draft`.

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

    multipleDevicesAndHoldersAllowedStatus: MultipleDevicesAndHoldersAllowedStatus = (
        MultipleDevicesAndHoldersAllowedStatus.STATUS_UNSPECIFIED
    )
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
    View Unlock Requirement options for the offer.
    """

    wideTitleImage: Optional[Image] = None
    """
    The wide title image of the offer. When provided, this will be used in
    place of the title image in the top left of the card view.
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

    merchantLocations: list[MerchantLocation] = Field(
        default_factory=list,
        max_length=10,
    )
    """
    Merchant locations. There is a maximum of ten on the class. Any additional
    MerchantLocations added beyond the 10 will be rejected. These locations
    will trigger a notification when a user enters within a Google-set radius
    of the point. This field replaces the deprecated LatLongPoints.
    """
