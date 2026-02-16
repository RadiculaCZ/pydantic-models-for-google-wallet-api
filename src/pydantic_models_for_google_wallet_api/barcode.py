# https://developers.google.com/wallet/reference/rest/v1/Barcode

from typing import Annotated, Literal, Optional

from pydantic import BaseModel
from typing_extensions import deprecated

from .barcode_render_encoding import BarcodeRenderEncoding
from .barcode_type import BarcodeType
from .localized_string import LocalizedString


class Barcode(BaseModel):
    kind: Annotated[
        Literal["walletobjects#barcode"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#barcode"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#barcode"`.
    """

    type: BarcodeType = BarcodeType.BARCODE_TYPE_UNSPECIFIED
    """
    The type of barcode.
    """

    renderEncoding: BarcodeRenderEncoding = (
        BarcodeRenderEncoding.RENDER_ENCODING_UNSPECIFIED
    )
    """
    The render encoding for the barcode. When specified, barcode is rendered in
    the given encoding. Otherwise best known encoding is chosen by Google.
    """

    value: str
    """
    The value encoded in the barcode.
    """

    alternateText: Optional[str] = None
    """
    An optional text that will override the default text that shows under the
    barcode. This field is intended for a human readable equivalent of the
    barcode value, used when the barcode cannot be scanned.
    """

    showCodeText: Optional[LocalizedString] = None
    """
    Optional text that will be shown when the barcode is hidden behind a click
    action. This happens in cases where a pass has Smart Tap enabled. If not
    specified, a default is chosen by Google.
    """
