# https://developers.google.com/wallet/reference/rest/v1/transitclass

from enum import Enum
from typing import Annotated, Optional

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


class TransitType(str, Enum):
    TRANSIT_TYPE_UNSPECIFIED = "TRANSIT_TYPE_UNSPECIFIED"

    BUS = "BUS"

    bus = "bus"
    """
    Legacy alias for `BUS`. Deprecated.
    """

    RAIL = "RAIL"

    rail = "rail"
    """
    Legacy alias for `RAIL`. Deprecated.
    """

    TRAM = "TRAM"

    tram = "tram"
    """
    Legacy alias for `TRAM`. Deprecated.
    """

    FERRY = "FERRY"

    ferry = "ferry"
    """
    Legacy alias for `FERRY`. Deprecated.
    """

    OTHER = "OTHER"

    other = "other"
    """
    Legacy alias for `OTHER`. Deprecated.
    """


class ActivationOptions(BaseModel):
    activationUrl: Optional[str] = Field(
        default=None,
        pattern=r"^https://.*$",
    )
    """
    HTTPS URL that supports REST semantics. Would be used for requesting
    activation from partners for given valuable, triggered by the users.
    """

    allowReactivation: bool = False
    """
    Flag to allow users to make activation call from different device. This
    allows client to render the activation button enabled even if the
    activationStatus is ACTIVATED but the requested device is different than
    the current device.
    """


class TransitClass(BaseModel):
    transitOperatorName: Optional[LocalizedString] = None
    """
    The name of the transit operator.
    """

    logo: Image
    """
    Required. The logo image of the ticket. This image is displayed in the card
    detail view of the app.
    """

    transitType: TransitType
    """
    Required. The type of transit this class represents, such as "bus".
    """

    watermark: Optional[Image] = None
    """
    Watermark image to display on the user's device.
    """

    languageOverride: Optional[str] = Field(
        default=None,
        pattern=r"^[a-z]{2}(-[A-Z]{2})?$",
    )
    """
    If this field is present, transit tickets served to a user's device will
    always be in this language. Represents the BCP 47 language tag. Example
    values are "en-US", "en-GB", "de", or "de-AT".
    """

    customTransitTerminusNameLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the transit terminus name value
    (`transitObject.ticketLeg.transitTerminusName`).
    """

    customTicketNumberLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the ticket number value
    (`transitObject.ticketNumber`).
    """

    customRouteRestrictionsLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the route restrictions value
    (`transitObject.ticketRestrictions.routeRestrictions`).
    """

    customRouteRestrictionsDetailsLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the route restrictions details value
    (`transitObject.ticketRestrictions.routeRestrictionsDetails`).
    """

    customTimeRestrictionsLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the time restrictions details value
    (`transitObject.ticketRestrictions.timeRestrictions`).
    """

    customOtherRestrictionsLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the other restrictions value
    (`transitObject.ticketRestrictions.otherRestrictions`).
    """

    customPurchaseReceiptNumberLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the purchase receipt number value
    (`transitObject.purchaseDetails.purchaseReceiptNumber`).
    """

    customConfirmationCodeLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the confirmation code value
    (`transitObject.purchaseDetails.confirmationCode`).
    """

    customPurchaseFaceValueLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the purchase face value
    (`transitObject.purchaseDetails.ticketCost.faceValue`).
    """

    customPurchasePriceLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the purchase price value
    (`transitObject.purchaseDetails.ticketCost.purchasePrice`).
    """

    customDiscountMessageLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the transit discount message value
    (`transitObject.purchaseDetails.ticketCost.discountMessage`).
    """

    customCarriageLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the carriage value
    (`transitObject.ticketLeg.carriage`).
    """

    customSeatLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the seat location value
    (`transitObject.ticketLeg.ticketSeat.seat`).
    """

    customCoachLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the coach value
    (`transitObject.ticketLeg.ticketSeat.coach`).
    """

    customPlatformLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the boarding platform value
    (`transitObject.ticketLeg.platform`).
    """

    customZoneLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the boarding zone value
    (`transitObject.ticketLeg.zone`).
    """

    customFareClassLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the fare class value
    (`transitObject.ticketLeg.ticketSeat.fareClass`).
    """

    customConcessionCategoryLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the transit concession category value
    (`transitObject.concessionCategory`).
    """

    customFareNameLabel: Optional[LocalizedString] = None
    """
    A custom label to use for the transit fare name value
    (`transitObject.ticketLeg.fareName`).
    """

    classTemplateInfo: Optional[ClassTemplateInfo] = None
    """
    Template information about how the class should be displayed. If unset,
    Google will fallback to a default set of fields to display.
    """

    enableSingleLegItinerary: bool = False
    """
    Controls the display of the single-leg itinerary for this class. By
    default, an itinerary will only display for multi-leg trips.
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
    Deprecated
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

    activationOptions: Optional[ActivationOptions] = None
    """
    Activation options for an activatable ticket.
    """

    viewUnlockRequirement: ViewUnlockRequirement = (
        ViewUnlockRequirement.VIEW_UNLOCK_REQUIREMENT_UNSPECIFIED
    )
    """
    View Unlock Requirement options for the transit ticket.
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
    part of an allowlist. If set to DO_NOT_NOTIFY or
    NOTIFICATION_SETTINGS_UNSPECIFIED, no notification will be triggered. This
    setting is ephemeral and needs to be set with each PATCH or UPDATE request,
    otherwise a notification will not be triggered.
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
