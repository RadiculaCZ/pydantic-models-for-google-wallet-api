# https://developers.google.com/wallet/reference/rest/v1/InfoModuleData

from typing import Annotated, Optional

from pydantic import BaseModel
from typing_extensions import deprecated

from .localized_string import LocalizedString


class LabelValue(BaseModel):
    label: str
    """
    The label for a specific row and column. Recommended maximum is 15
    characters for a two-column layout and 30 characters for a one-column
    layout.
    """

    value: str
    """
    The value for a specific row and column. Recommended maximum is 15
    characters for a two-column layout and 30 characters for a one-column
    layout.
    """

    localizedLabel: LocalizedString
    """
    Translated strings for the label. Recommended maximum is 15 characters for
    a two-column layout and 30 characters for a one-column layout.
    """

    localizedValue: LocalizedString
    """
    Translated strings for the value. Recommended maximum is 15 characters for
    a two-column layout and 30 characters for a one-column layout.
    """


class LabelValueRow(BaseModel):
    columns: list[LabelValue]
    """
    A list of labels and values. These will be displayed in a singular column,
    one after the other, not in multiple columns, despite the field name.
    """


class InfoModuleData(BaseModel):
    labelValueRows: list[LabelValueRow]
    """
    A list of collections of labels and values. These will be displayed one
    after the other in a singular column.
    """

    showLastUpdateTime: Annotated[
        Optional[bool],
        deprecated("This item is deprecated!"),
    ] = None
