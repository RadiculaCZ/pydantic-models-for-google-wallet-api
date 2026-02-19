# https://developers.google.com/wallet/reference/rest/v1/ValueAddedModuleData

from typing import Optional

from pydantic import BaseModel

from .image import Image
from .localized_string import LocalizedString
from .time_interval import TimeInterval


class ModuleViewConstraints(BaseModel):
    """
    Constraints that all must be met for the module to be shown.
    """

    displayInterval: TimeInterval
    """
    The period of time that the module will be displayed to users. Can define
    both a `startTime` and `endTime`. The module is displayed immediately after
    insertion unless a `startTime` is set. The module is displayed indefinitely
    if `endTime` is not set.
    """


class ValueAddedModuleData(BaseModel):
    """
    Data for Value Added module. Required fields are header and uri.
    """

    header: LocalizedString
    """
    Header to be displayed on the module. Character limit is 60 and longer
    strings will be truncated.
    """

    body: Optional[LocalizedString] = None
    """
    Body to be displayed on the module. Character limit is 50 and longer
    strings will be truncated.
    """

    image: Optional[Image] = None
    """
    Image to be displayed on the module. Recommended image ratio is 1:1. Images
    will be resized to fit this ratio.
    """

    uri: str
    """
    URI that the module leads to on click. This can be a web link or a deep
    link as mentioned in
    https://developer.android.com/training/app-links/deep-linking.
    """

    viewConstraints: Optional[ModuleViewConstraints] = None
    """
    Constraints that all must be met for the module to be shown.
    """

    sortIndex: Optional[int] = None
    """
    The index for sorting the modules. Modules with a lower sort index are
    shown before modules with a higher sort index. If unspecified, the sort
    index is assumed to be INT_MAX. For two modules with the same index, the
    sorting behavior is undefined.
    """
