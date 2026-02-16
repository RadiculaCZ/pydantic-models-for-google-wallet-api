# https://developers.google.com/wallet/reference/rest/v1/TextModuleData

from typing import Optional

from pydantic import BaseModel

from .localized_string import LocalizedString


class TextModuleData(BaseModel):
    """
    Data for Text module. All fields are optional. Header will be displayed if
    available, different types of bodies will be concatenated if they are
    defined.
    """

    header: Optional[str] = None
    """
    The header of the Text Module. Recommended maximum length is 35 characters
    to ensure full string is displayed on smaller screens.
    """

    body: Optional[str] = None
    """
    The body of the Text Module, which is defined as an uninterrupted string.
    Recommended maximum length is 500 characters to ensure full string is
    displayed on smaller screens.
    """

    localizedHeader: Optional[LocalizedString] = None
    """
    Translated strings for the header. Recommended maximum length is 35
    characters to ensure full string is displayed on smaller screens.
    """

    localizedBody: Optional[LocalizedString] = None
    """
    Translated strings for the body. Recommended maximum length is 500
    characters to ensure full string is displayed on smaller screens.
    """

    id: Optional[str] = None
    """
    The ID associated with a text module. This field is here to enable ease of
    management of text modules and referencing them in template overrides. The
    ID should only include alphanumeric characters, '_', or '-'. It can not
    include dots, as dots are used to separate fields within
    FieldReference.fieldPaths in template overrides.
    """
