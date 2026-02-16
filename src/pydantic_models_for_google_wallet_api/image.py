# https://developers.google.com/wallet/reference/rest/v1/Image

from typing import Annotated, Literal, Optional

from pydantic import BaseModel
from typing_extensions import deprecated

from .localized_string import LocalizedString


class ImageUri(BaseModel):
    uri: str
    """
    The location of the image. URIs must have a scheme.
    """

    description: Annotated[
        Optional[str], deprecated("This item is deprecated!")
    ] = None
    """
    Additional information about the image, which is unused and retained only
    for backward compatibility.
    """

    localizedDescription: Annotated[
        Optional[LocalizedString],
        deprecated("This item is deprecated!"),
    ] = None
    """
    Translated strings for the description, which are unused and retained only
    for backward compatibility.
    """


class Image(BaseModel):
    """
    Wrapping type for Google hosted images.
    """

    kind: Annotated[
        Literal["walletobjects#image"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#image"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#image"`.
    """

    sourceUri: ImageUri
    """
    The URI for the image.
    """

    contentDescription: LocalizedString
    """
    Description of the image used for accessibility.
    """
