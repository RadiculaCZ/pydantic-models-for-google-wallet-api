# https://developers.google.com/wallet/reference/rest/v1/ClassTemplateInfo

from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel
from typing_extensions import deprecated


class DateFormat(str, Enum):
    """
    DateFormat options specific to rendering date/time fields.
    """

    DATE_FORMAT_UNSPECIFIED = "DATE_FORMAT_UNSPECIFIED"
    """
    Default option when no format is specified, when selected, no formatting
    will be applied.
    """

    DATE_TIME = "DATE_TIME"
    """
    Renders `2018-12-14T13:00:00` as `Dec 14, 1:00 PM` in `en_US`.
    """

    dateTime = "dateTime"
    """
    Legacy alias for `DATE_TIME`. Deprecated.
    """

    DATE_ONLY = "DATE_ONLY"
    """
    Renders `2018-12-14T13:00:00` as `Dec 14` in `en_US`.
    """

    dateOnly = "dateOnly"
    """
    Legacy alias for `DATE_ONLY`. Deprecated.
    """

    TIME_ONLY = "TIME_ONLY"
    """
    Renders `2018-12-14T13:00:00` as `1:00 PM` in `en_US`.
    """

    timeOnly = "timeOnly"
    """
    Legacy alias for `TIME_ONLY`. Deprecated.
    """

    DATE_TIME_YEAR = "DATE_TIME_YEAR"
    """
    Renders `2018-12-14T13:00:00` as `Dec 14, 2018, 1:00 PM` in `en_US`.
    """

    dateTimeYear = "dateTimeYear"
    """
    Legacy alias for `DATE_TIME_YEAR`. Deprecated.
    """

    DATE_YEAR = "DATE_YEAR"
    """
    Renders `2018-12-14T13:00:00` as `Dec 14, 2018` in `en_US`.
    """

    dateYear = "dateYear"
    """
    Legacy alias for `DATE_YEAR`. Deprecated.
    """

    YEAR_MONTH = "YEAR_MONTH"
    """
    Renders `2018-12-14T13:00:00` as `2018-12`.
    """

    YEAR_MONTH_DAY = "YEAR_MONTH_DAY"
    """
    Renders `2018-12-14T13:00:00` as `2018-12-14`.
    """


class FieldReference(BaseModel):
    """
    Reference definition to use with field overrides.
    """

    fieldPath: str
    """
    Path to the field being referenced, prefixed with "object" or "class" and
    separated with dots. For example, it may be the string
    "object.purchaseDetails.purchasePrice".
    """

    dateFormat: DateFormat = DateFormat.DATE_FORMAT_UNSPECIFIED
    """
    Only valid if the `fieldPath` references a date field. Chooses how the date
    field will be formatted and displayed in the UI.
    """


class FieldSelector(BaseModel):
    """
    Custom field selector to use with field overrides.
    """

    fields: list[FieldReference]
    """
    If more than one reference is supplied, then the first one that references
    a non-empty field will be displayed.
    """


class BarcodeSectionDetail(BaseModel):
    fieldSelector: FieldSelector
    """
    A reference to an existing text-based or image field to display.
    """


class CardBarcodeSectionDetails(BaseModel):
    firstTopDetail: Optional[BarcodeSectionDetail] = None
    """
    Optional information to display above the barcode. If `secondTopDetail` is
    defined, this will be displayed to the start side of this detail section.
    """

    firstBottomDetail: Optional[BarcodeSectionDetail] = None
    """
    Optional information to display below the barcode.
    """

    secondTopDetail: Optional[BarcodeSectionDetail] = None
    """
    Optional second piece of information to display above the barcode. If
    `firstTopDetail` is defined, this will be displayed to the end side of this
    detail section.
    """


class PredefinedItem(str, Enum):
    PREDEFINED_ITEM_UNSPECIFIED = "PREDEFINED_ITEM_UNSPECIFIED"

    FREQUENT_FLYER_PROGRAM_NAME_AND_NUMBER = (
        "FREQUENT_FLYER_PROGRAM_NAME_AND_NUMBER"
    )

    frequentFlyerProgramNameAndNumber = "frequentFlyerProgramNameAndNumber"
    """
    Legacy alias for `FREQUENT_FLYER_PROGRAM_NAME_AND_NUMBER`. Deprecated.
    """

    FLIGHT_NUMBER_AND_OPERATING_FLIGHT_NUMBER = (
        "FLIGHT_NUMBER_AND_OPERATING_FLIGHT_NUMBER"
    )

    flightNumberAndOperatingFlightNumber = (
        "flightNumberAndOperatingFlightNumber"
    )
    """
    Legacy alias for `FLIGHT_NUMBER_AND_OPERATING_FLIGHT_NUMBER`. Deprecated.
    """


class TemplateItem(BaseModel):
    firstValue: Optional[FieldSelector] = None
    """
    A reference to a field to display. If both `firstValue` and `secondValue`
    are populated, they will both appear as one item with a slash between them.
    For example, values A and B would be shown as "A / B".
    """

    secondValue: Optional[FieldSelector] = None
    """
    A reference to a field to display. This may only be populated if the
    `firstValue` field is populated.
    """

    predefinedItem: PredefinedItem = PredefinedItem.PREDEFINED_ITEM_UNSPECIFIED
    """
    A predefined item to display. Only one of `firstValue` or `predefinedItem`
    may be set.
    """


class CardRowOneItem(BaseModel):
    item: TemplateItem
    """
    The item to be displayed in the row. This item will be automatically
    centered.
    """


class CardRowTwoItems(BaseModel):
    startItem: TemplateItem
    """
    The item to be displayed at the start of the row. This item will be aligned
    to the left.
    """

    endItem: TemplateItem
    """
    The item to be displayed at the end of the row. This item will be aligned
    to the right.
    """


class CardRowThreeItems(BaseModel):
    startItem: TemplateItem
    """
    The item to be displayed at the start of the row. This item will be aligned
    to the left.
    """

    middleItem: TemplateItem
    """
    The item to be displayed in the middle of the row. This item will be
    centered between the start and end items.
    """

    endItem: TemplateItem
    """
    The item to be displayed at the end of the row. This item will be aligned
    to the right.
    """


class CardRowTemplateInfo(BaseModel):
    oneItem: Optional[CardRowOneItem] = None
    """
    Template for a row containing one item. Exactly one of "oneItem",
    "twoItems", "threeItems" must be set.
    """

    twoItems: Optional[CardRowTwoItems] = None
    """
    Template for a row containing two items. Exactly one of "oneItem",
    "twoItems", "threeItems" must be set.
    """

    threeItems: Optional[CardRowThreeItems] = None
    """
    Template for a row containing three items. Exactly one of "oneItem",
    "twoItems", "threeItems" must be set.
    """


class CardTemplateOverride(BaseModel):
    cardRowTemplateInfos: list[CardRowTemplateInfo]
    """
    Template information for rows in the card view. At most three rows are
    allowed to be specified.
    """


class DetailsItemInfo(BaseModel):
    item: TemplateItem
    """
    The item to be displayed in the details list.
    """


class DetailsTemplateOverride(BaseModel):
    detailsItemInfos: list[DetailsItemInfo]
    """
    Information for the "nth" item displayed in the details list.
    """


class TransitOption(str, Enum):
    TRANSIT_OPTION_UNSPECIFIED = "TRANSIT_OPTION_UNSPECIFIED"

    ORIGIN_AND_DESTINATION_NAMES = "ORIGIN_AND_DESTINATION_NAMES"

    originAndDestinationNames = "originAndDestinationNames"
    """
    Legacy alias for `ORIGIN_AND_DESTINATION_NAMES`. Deprecated.
    """

    ORIGIN_AND_DESTINATION_CODES = "ORIGIN_AND_DESTINATION_CODES"

    originAndDestinationCodes = "originAndDestinationCodes"
    """
    Legacy alias for `ORIGIN_AND_DESTINATION_CODES`. Deprecated.
    """

    ORIGIN_NAME = "ORIGIN_NAME"

    originName = "originName"
    """
    Legacy alias for `ORIGIN_NAME`. Deprecated.
    """


class FirstRowOption(BaseModel):
    transitOption: TransitOption

    fieldOption: FieldSelector
    """
    A reference to the field to be displayed in the first row.
    """


class ListTemplateOverride(BaseModel):
    firstRowOption: Optional[FirstRowOption] = None
    """
    Specifies from a predefined set of options or from a reference to the field
    what will be displayed in the first row. To set this override, set the
    FirstRowOption.fieldOption to the FieldSelector of your choice.
    """

    secondRowOption: Optional[FieldSelector] = None
    """
    A reference to the field to be displayed in the second row.

    This option is only displayed if there are not multiple user objects in a
    group. If there is a group, the second row will always display a field
    shared by all objects. To set this override, please set secondRowOption to
    the FieldSelector of you choice.
    """

    thirdRowOption: Annotated[
        Optional[FieldSelector],
        deprecated("This item is deprecated!"),
    ] = None
    """
    An unused/deprecated field. Setting it will have no effect on what the user
    sees.
    """


class ClassTemplateInfo(BaseModel):
    cardBarcodeSectionDetails: Optional[CardBarcodeSectionDetails] = None
    """
    Specifies extra information to be displayed above and below the barcode.
    """

    cardTemplateOverride: Optional[CardTemplateOverride] = None
    """
    Override for the card view.
    """

    detailsTemplateOverride: Optional[DetailsTemplateOverride] = None
    """
    Override for the details view (beneath the card view).
    """

    listTemplateOverride: Optional[ListTemplateOverride] = None
    """
    Override for the passes list view.
    """
