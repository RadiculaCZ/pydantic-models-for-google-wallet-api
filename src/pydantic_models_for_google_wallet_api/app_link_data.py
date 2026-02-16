# https://developers.google.com/wallet/reference/rest/v1/AppLinkData

from typing import Annotated, Optional

from pydantic import BaseModel
from typing_extensions import deprecated

from .image import Image
from .localized_string import LocalizedString
from .uri import Uri


class AppTarget(BaseModel):
    """
    Union field target.

    target can be only one of the following:
    """

    targetUri: Optional[Uri] = None
    """
    URI for AppTarget. The description on the URI must be set. Prefer setting
    package field instead, if this target is defined for your application.
    """

    packageName: Optional[str] = None
    """
    Package name for AppTarget. For example: com.google.android.gm
    """


class AppLinkInfo(BaseModel):
    appLogoImage: Annotated[
        Optional[Image], deprecated("This item is deprecated!")
    ] = None
    """
    Deprecated. Image isn't supported in the app link module.
    """

    title: Annotated[
        Optional[LocalizedString], deprecated("This item is deprecated!")
    ] = None
    """
    Deprecated. Title isn't supported in the app link module.
    """

    description: Annotated[
        Optional[LocalizedString], deprecated("This item is deprecated!")
    ] = None
    """
    Deprecated. Description isn't supported in the app link module.
    """

    appTarget: AppTarget
    """
    Target to follow when opening the app link on clients. It will be used by
    partners to open their app or webpage.
    """


class AppLinkData(BaseModel):
    androidAppLinkInfo: Optional[AppLinkInfo] = None
    """
    Optional information about the partner app link.
    """

    iosAppLinkInfo: Annotated[
        Optional[AppLinkInfo],
        deprecated("This item is deprecated!"),
    ] = None
    """
    Deprecated. Links to open iOS apps are not supported.
    """

    webAppLinkInfo: Optional[AppLinkInfo] = None
    """
    Optional information about the partner web link.
    """

    displayText: Optional[LocalizedString] = None
    """
    Optional display text for the app link button. Character limit is 30.
    """
