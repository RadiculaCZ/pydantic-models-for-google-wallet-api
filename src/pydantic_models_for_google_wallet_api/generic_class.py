# https://developers.google.com/wallet/reference/rest/v1/genericclass

from typing import Optional

from pydantic import BaseModel, Field

from .app_link_data import AppLinkData
from .callback_options import CallbackOptions
from .class_template_info import ClassTemplateInfo
from .image_module_data import ImageModuleData
from .links_module_data import LinksModuleData
from .merchant_location import MerchantLocation
from .message import Message
from .multiple_devices_and_holders_allowed_status import (
    MultipleDevicesAndHoldersAllowedStatus,
)
from .security_animation import SecurityAnimation
from .text_module_data import TextModuleData
from .value_added_module_data import ValueAddedModuleData
from .view_unlock_requirement import ViewUnlockRequirement


class GenericClass(BaseModel):
    """
    Generic Class
    """

    id: str
    """
    Required. The unique identifier for the class. This ID must be unique
    across all from an issuer. This value needs to follow the format
    `issuerID.identifier` where `issuerID` is issued by Google and `identifier`
    is chosen by you. The unique identifier can only include alphanumeric
    characters, `.`, `_`, or `-`.
    """

    classTemplateInfo: Optional[ClassTemplateInfo] = None
    """
    Template information about how the class should be displayed. If unset,
    Google will fallback to a default set of fields to display.
    """

    imageModulesData: list[ImageModuleData] = Field(default_factory=list)
    """
    Image module data. If `imageModulesData` is also defined on the object,
    both will be displayed. Only one of the image from class and one from
    object level will be rendered when both set.
    """

    textModulesData: list[TextModuleData] = Field(default_factory=list)
    """
    Text module data. If `textModulesData` is also defined on the object, both
    will be displayed. The maximum number of these fields displayed is 10 from
    class and 10 from object.
    """

    linksModuleData: list[LinksModuleData] = Field(default_factory=list)
    """
    Links module data. If `linksModuleData` is also defined on the object, both
    will be displayed. The maximum number of these fields displayed is 10 from
    class and 10 from object.
    """

    enableSmartTap: bool = False
    """
    Available only to Smart Tap enabled partners. Contact support for
    additional guidance.
    """

    redemptionIssuers: list[str] = Field(default_factory=list)
    """
    Identifies which redemption issuers can redeem the pass over Smart Tap.
    Redemption issuers are identified by their issuer ID. Redemption issuers
    must have at least one Smart Tap key configured.

    The `enableSmartTap` and object level `smartTapRedemptionLevel` fields must
    also be set up correctly in order for a pass to support Smart Tap.
    """

    securityAnimation: Optional[SecurityAnimation] = None
    """
    Optional information about the security animation. If this is set a
    security animation will be rendered on pass details.
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

    viewUnlockRequirement: ViewUnlockRequirement = (
        ViewUnlockRequirement.VIEW_UNLOCK_REQUIREMENT_UNSPECIFIED
    )
    """
    View Unlock Requirement options for the generic pass.
    """

    messages: list[Message] = Field(default_factory=list, max_length=10)
    """
    An array of messages displayed in the app. All users of this object will
    receive its associated messages. The maximum number of these fields is 10.
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

    merchantLocations: list[MerchantLocation] = Field(default_factory=list)
    """
    Merchant locations. There is a maximum of ten on the class. Any additional
    MerchantLocations added beyond the 10 will be rejected. These locations
    will trigger a notification when a user enters within a Google-set radius
    of the point. This field replaces the deprecated LatLongPoints.
    """
