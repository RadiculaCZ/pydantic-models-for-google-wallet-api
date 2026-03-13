# https://developers.google.com/wallet/reference/rest/v1/loyaltyclass

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


class SharedDataType(str, Enum):
    SHARED_DATA_TYPE_UNSPECIFIED = "SHARED_DATA_TYPE_UNSPECIFIED"

    FIRST_NAME = "FIRST_NAME"

    LAST_NAME = "LAST_NAME"

    STREET_ADDRESS = "STREET_ADDRESS"
    """
    single line address field
    """

    ADDRESS_LINE_1 = "ADDRESS_LINE_1"
    """
    multi line address fields
    """

    ADDRESS_LINE_2 = "ADDRESS_LINE_2"

    ADDRESS_LINE_3 = "ADDRESS_LINE_3"

    CITY = "CITY"

    STATE = "STATE"

    ZIPCODE = "ZIPCODE"

    COUNTRY = "COUNTRY"

    EMAIL = "EMAIL"

    PHONE = "PHONE"


class DiscoverableProgramMerchantSignupInfo(BaseModel):
    """
    Information about the merchant hosted signup flow for a program.
    """

    signupWebsite: Optional[Uri] = None
    """
    The URL to direct the user to for the merchant's signup site.
    """

    signupSharedDatas: list[SharedDataType] = Field(default_factory=list)
    """
    User data that is sent in a POST request to the signup website URL. This
    information is encoded and then shared so that the merchant's website can
    prefill fields used to enroll the user for the discoverable program.
    """


class DiscoverableProgramMerchantSigninInfo(BaseModel):
    """
    Information about the merchant hosted signin flow for a program.
    """

    signinWebsite: Optional[Uri] = None
    """
    The URL to direct the user to for the merchant's signin site.
    """


class State(str, Enum):
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"

    TRUSTED_TESTERS = "TRUSTED_TESTERS"
    """
    Visible only to testers that have access to issuer account.
    """

    trustedTesters = "trustedTesters"
    """
    Legacy alias for `TRUSTED_TESTERS`. Deprecated.
    """

    LIVE = "LIVE"
    """
    Visible to all.
    """

    live = "live"
    """
    Legacy alias for `LIVE`. Deprecated.
    """

    DISABLED = "DISABLED"
    """
    Not visible.
    """

    disabled = "disabled"
    """
    Legacy alias for `DISABLED`. Deprecated.
    """


class DiscoverableProgram(BaseModel):
    """
    Information about how a class may be discovered and instantiated from
    within the Google Wallet app. This is done by searching for a loyalty or
    gift card program and scanning or manually entering.
    """

    merchantSignupInfo: Optional[DiscoverableProgramMerchantSignupInfo] = None
    """
    Information about the ability to signup and add a valuable for this program
    through a merchant site. Used when MERCHANT_HOSTED_SIGNUP is enabled.
    """

    merchantSigninInfo: Optional[DiscoverableProgramMerchantSigninInfo] = None
    """
    Information about the ability to signin and add a valuable for this program
    through a merchant site. Used when MERCHANT_HOSTED_SIGNIN is enabled.
    """

    state: State = State.STATE_UNSPECIFIED
    """
    Visibility state of the discoverable program.
    """


class LoyaltyClass(BaseModel):
    kind: Annotated[
        Literal["walletobjects#loyaltyClass"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#loyaltyClass"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#loyaltyClass"`.
    """

    programName: str
    """
    Required. The program name, such as "Adam's Apparel". The app may display
    an ellipsis after the first 20 characters to ensure full string is
    displayed on smaller screens.
    """

    programLogo: Image
    """
    Required. The logo of the loyalty program or company. This logo is
    displayed in both the details and list views of the app.
    """

    accountNameLabel: Optional[str] = None
    """
    The account name label, such as "Member Name." Recommended maximum length
    is 15 characters to ensure full string is displayed on smaller screens.
    """

    accountIdLabel: Optional[str] = None
    """
    The account ID label, such as "Member ID." Recommended maximum length is
    15 characters to ensure full string is displayed on smaller screens.
    """

    rewardsTierLabel: Optional[str] = None
    """
    The rewards tier label, such as "Rewards Tier." Recommended maximum length
    is 9 characters to ensure full string is displayed on smaller screens.
    """

    rewardsTier: Optional[str] = None
    """
    The rewards tier, such as "Gold" or "Platinum." Recommended maximum length
    is 7 characters to ensure full string is displayed on smaller screens.
    """

    localizedProgramName: Optional[LocalizedString] = None
    """
    Translated strings for the programName. The app may display an ellipsis
    after the first 20 characters to ensure full string is displayed on smaller
    screens.
    """

    localizedAccountNameLabel: Optional[LocalizedString] = None
    """
    Translated strings for the accountNameLabel. Recommended maximum length is
    15 characters to ensure full string is displayed on smaller screens.
    """

    localizedAccountIdLabel: Optional[LocalizedString] = None
    """
    Translated strings for the accountIdLabel. Recommended maximum length is 15
    characters to ensure full string is displayed on smaller screens.
    """

    localizedRewardsTierLabel: Optional[LocalizedString] = None
    """
    Translated strings for the rewardsTierLabel. Recommended maximum length is
    9 characters to ensure full string is displayed on smaller screens.
    """

    localizedRewardsTier: Optional[LocalizedString] = None
    """
    Translated strings for the rewardsTier. Recommended maximum length is 7
    characters to ensure full string is displayed on smaller screens.
    """

    secondaryRewardsTierLabel: Optional[str] = None
    """
    The secondary rewards tier label, such as "Rewards Tier."
    """

    localizedSecondaryRewardsTierLabel: Optional[LocalizedString] = None
    """
    Translated strings for the secondaryRewardsTierLabel.
    """

    secondaryRewardsTier: Optional[str] = None
    """
    The secondary rewards tier, such as "Gold" or "Platinum."
    """

    localizedSecondaryRewardsTier: Optional[LocalizedString] = None
    """
    Translated strings for the secondaryRewardsTier.
    """

    discoverableProgram: Optional[DiscoverableProgram] = None
    """
    Information about how the class may be discovered and instantiated from
    within the Google Pay app.
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

    messages: list[Message] = Field(default_factory=list)
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
    Identifies which redemption issuers can redeem the pass over Smart Tap.
    Redemption issuers are identified by their issuer ID. Redemption issuers
    must have at least one Smart Tap key configured.

    The `enableSmartTap` and one of object level `smartTapRedemptionValue`,
    `barcode.value`, or `accountId` fields must also be set up correctly in
    order for a pass to support Smart Tap.
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
    and one of object level `smartTapRedemptionLevel`, `barcode.value`, or
    `accountId` fields must also be set up correctly in order for a pass to
    support Smart Tap.
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
    View Unlock Requirement options for the loyalty card.
    """

    wideProgramLogo: Optional[Image] = None
    """
    The wide logo of the loyalty program or company. When provided, this will
    be used in place of the program logo in the top left of the card view.
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
