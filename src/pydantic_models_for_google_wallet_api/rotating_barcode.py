# https://developers.google.com/wallet/reference/rest/v1/RotatingBarcode

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from .barcode_render_encoding import BarcodeRenderEncoding
from .barcode_type import BarcodeType
from .localized_string import LocalizedString


class TotpAlgorithm(str, Enum):
    TOTP_ALGORITHM_UNSPECIFIED = "TOTP_ALGORITHM_UNSPECIFIED"

    TOTP_SHA1 = "TOTP_SHA1"
    """
    TOTP algorithm from RFC 6238 with the SHA1 hash function
    """


class TotpParameters(BaseModel):
    """
    Configuration for the key and value length. See
    https://www.rfc-editor.org/rfc/rfc4226#section-5.3
    """

    key: str
    """
    The secret key used for the TOTP value generation, encoded as a Base16
    string.
    """

    valueLength: int = Field(..., gt=0)
    """
    The length of the TOTP value in decimal digits.
    """


class TotpDetails(BaseModel):
    """
    Configuration for the time-based OTP substitutions. See
    https://tools.ietf.org/html/rfc6238
    """

    periodMillis: str
    """
    int64 format

    The time interval used for the TOTP value generation, in milliseconds.
    """

    algorithm: TotpAlgorithm = TotpAlgorithm.TOTP_ALGORITHM_UNSPECIFIED
    """
    The TOTP algorithm used to generate the OTP.
    """

    parameters: list[TotpParameters] = []
    """
    The TOTP parameters for each of the {totp_value_*} substitutions. The
    TotpParameters at index n is used for the {totp_value_n} substitution.
    """


class RotatingBarcodeValues(BaseModel):
    """
    A payload containing many barcode values and start date/time.
    """

    startDateTime: str  # See DateTime type as well
    """
    Required. The date/time the first barcode is valid from. Barcodes will be
    rotated through using periodMillis defined on the object's
    RotatingBarcodeValueInfo.

    This is an ISO 8601 extended format date/time, with an offset. Time may be
    specified up to nanosecond precision. Offsets may be specified with seconds
    precision (even though offset seconds is not part of ISO 8601).

    For example:

    `1985-04-12T23:20:50.52Z` would be 20 minutes and 50.52 seconds after the
    23rd hour of April 12th, 1985 in UTC.

    `1985-04-12T19:20:50.52-04:00` would be 20 minutes and 50.52 seconds after
    the 19th hour of April 12th, 1985, 4 hours before UTC (same instant in time
    as the above example). If the event were in New York, this would be the
    equivalent of Eastern Daylight Time (EDT). Remember that offset varies in
    regions that observe Daylight Saving Time (or Summer Time), depending on
    the time of the year.
    """

    values: list[str]
    """
    Required. The values to encode in the barcode. At least one value is
    required.
    """

    periodMillis: str
    """
    int64 format

    Required. The amount of time each barcode is valid for.
    """


class RotatingBarcode(BaseModel):
    type: BarcodeType = BarcodeType.BARCODE_TYPE_UNSPECIFIED
    """
    The type of this barcode.
    """

    renderEncoding: BarcodeRenderEncoding = (
        BarcodeRenderEncoding.RENDER_ENCODING_UNSPECIFIED
    )
    """
    The render encoding for the barcode. When specified, barcode is rendered in
    the given encoding. Otherwise best known encoding is chosen by Google.
    """

    valuePattern: str
    """
    String encoded barcode value. This string supports the following
    substitutions:
    * {totp_value_n}: Replaced with the TOTP value (see
      TotpDetails.parameters).
    * {totp_timestamp_millis}: Replaced with the timestamp (millis since epoch)
      at which the barcode was generated.
    * {totp_timestamp_seconds}: Replaced with the timestamp (seconds since
      epoch) at which the barcode was generated.
    """

    totpDetails: TotpDetails
    """
    Details used to evaluate the {totp_value_n} substitutions.
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

    initialRotatingBarcodeValues: Optional[RotatingBarcodeValues] = None
    """
    Input only. NOTE: This feature is only available for the transit vertical.
    Optional set of initial rotating barcode values. This allows a small subset
    of barcodes to be included with the object. Further rotating barcode values
    must be uploaded with the UploadRotatingBarcodeValues endpoint.
    """
