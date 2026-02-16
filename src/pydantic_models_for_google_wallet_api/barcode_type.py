# https://developers.google.com/wallet/reference/rest/v1/BarcodeType

from enum import Enum


class BarcodeType(str, Enum):
    BARCODE_TYPE_UNSPECIFIED = "BARCODE_TYPE_UNSPECIFIED"

    AZTEC = "AZTEC"
    """
    Not supported for Rotating Barcodes.
    """

    aztec = "aztec"
    """
    Legacy alias for `AZTEC`. Deprecated. Not supported for Rotating Barcodes.
    """

    CODE_39 = "CODE_39"
    """
    Not supported for Rotating Barcodes.
    """

    code39 = "code39"
    """
    Legacy alias for `CODE_39`. Deprecated. Not supported for Rotating
    Barcodes.
    """

    CODE_128 = "CODE_128"
    """
    Not supported for Rotating Barcodes.
    """

    code128 = "code128"
    """
    Legacy alias for `CODE_128`. Deprecated. Not supported for Rotating
    Barcodes.
    """

    CODABAR = "CODABAR"
    """
    Not supported for Rotating Barcodes.
    """

    codabar = "codabar"
    """
    Legacy alias for `CODABAR`. Deprecated. Not supported for Rotating Barcodes.
    """

    DATA_MATRIX = "DATA_MATRIX"
    """
    A 2D matrix barcode consisting of black and white. Cells or modules are
    arranged in either a square or rectangle. Not supported for Rotating
    Barcodes.
    """

    dataMatrix = "dataMatrix"
    """
    Legacy alias for `DATA_MATRIX`. Deprecated. Not supported for Rotating
    Barcodes.
    """

    EAN_8 = "EAN_8"
    """
    Not supported for Rotating Barcodes.
    """

    ean8 = "ean8"
    """
    Legacy alias for `EAN_8`. Deprecated. Not supported for Rotating Barcodes.
    """

    EAN_13 = "EAN_13"
    """
    Not supported for Rotating Barcodes.
    """

    ean13 = "ean13"
    """
    Legacy alias for `EAN_13`. Deprecated. Not supported for Rotating Barcodes.
    """

    EAN13 = "EAN13"
    """
    Legacy alias for `EAN_13`. Deprecated. Not supported for Rotating Barcodes.
    """

    ITF_14 = "ITF_14"
    """
    14 digit ITF code Not supported for Rotating Barcodes.
    """

    itf14 = "itf14"
    """
    Legacy alias for `ITF_14`. Deprecated. Not supported for Rotating Barcodes.
    """

    PDF_417 = "PDF_417"
    """
    Supported for Rotating Barcodes.
    """

    pdf417 = "pdf417"
    """
    Legacy alias for `PDF_417`. Deprecated.
    """

    PDF417 = "PDF417"
    """
    Legacy alias for `PDF_417`. Deprecated.
    """

    QR_CODE = "QR_CODE"
    """
    Supported for Rotating Barcodes.
    """

    qrCode = "qrCode"
    """
    Legacy alias for `QR_CODE`. Deprecated.
    """

    qrcode = "qrcode"
    """
    Legacy alias for `QR_CODE`. Deprecated.
    """

    UPC_A = "UPC_A"
    """
    11 or 12 digit codes Not supported for Rotating Barcodes.
    """

    upcA = "upcA"
    """
    Legacy alias for `UPC_A`. Deprecated. Not supported for Rotating Barcodes.
    """

    TEXT_ONLY = "TEXT_ONLY"
    """
    Renders the field as a text field. The `alternateText` field may not be
    used with a barcode of type `textOnly`. Not supported for Rotating
    Barcodes.
    """

    textOnly = "textOnly"
    """
    Legacy alias for `TEXT_ONLY`. Deprecated. Not supported for Rotating
    Barcodes.
    """
