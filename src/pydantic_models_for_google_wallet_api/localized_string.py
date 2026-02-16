# https://developers.google.com/wallet/reference/rest/v1/LocalizedString

from typing import Annotated, Literal

from pydantic import BaseModel, Field
from typing_extensions import deprecated


class TranslatedString(BaseModel):
    kind: Annotated[
        Literal["walletobjects#translatedString"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#translatedString"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#translatedString"`.
    """

    language: str = Field(
        ...,
        min_length=2,
        # See https://en.wikipedia.org/wiki/IETF_language_tag#Syntax_of_language_tags
        pattern=r"^[a-z]{2,3}(-[a-z]{3}){0,3}(-[A-Z][a-z]{3})?(-([A-Z]{2}|\d{3}))?(-([a-z]{5,8}|\d[a-z]{3}))*(-[a-wyz](-[a-z]{2,8})+)*(-x(-[a-z]{1,8})+)?$",
    )
    """
    Represents the BCP 47 language tag. Example values are "en-US", "en-GB",
    "de", or "de-AT".
    """

    value: str
    """
    The UTF-8 encoded translated string.
    """


class LocalizedString(BaseModel):
    kind: Annotated[
        Literal["walletobjects#localizedString"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#localizedString"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#localizedString"`.
    """

    translatedValues: list[TranslatedString]
    """
    Contains the translations for the string.
    """

    defaultValue: TranslatedString
    """
    Contains the string to be displayed if no appropriate translation is
    available.
    """
