# https://developers.google.com/wallet/reference/rest/v1/Uri
from typing import Annotated, Literal, Optional

from pydantic import BaseModel
from typing_extensions import deprecated

from .localized_string import LocalizedString


class Uri(BaseModel):
    kind: Annotated[
        Literal["walletobjects#uri"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#uri"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#uri"`.
    """

    uri: str
    """
    The location of a web page, image, or other resource. URIs in the
    `LinksModuleData` module can have different prefixes indicating the type of
    URI (a link to a web page, a link to a map, a telephone number, or an email
    address). URIs must have a scheme.
    """

    description: Optional[str] = None
    """
    The URI's title appearing in the app as text. Recommended maximum is 20
    characters to ensure full string is displayed on smaller screens.

    Note that in some contexts this text is not used, such as when
    `description` is part of an image.
    """

    localizedDescription: Optional[LocalizedString] = None
    """
    Translated strings for the description. Recommended maximum is 20
    characters to ensure full string is displayed on smaller screens.
    """

    id: Optional[str] = None
    """
    The ID associated with a uri. This field is here to enable ease of
    management of uris.
    """
