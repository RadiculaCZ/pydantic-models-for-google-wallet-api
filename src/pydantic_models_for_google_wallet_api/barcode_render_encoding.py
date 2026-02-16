# https://developers.google.com/wallet/reference/rest/v1/BarcodeRenderEncoding

from enum import Enum


class BarcodeRenderEncoding(str, Enum):
    RENDER_ENCODING_UNSPECIFIED = "RENDER_ENCODING_UNSPECIFIED"

    UTF_8 = "UTF_8"
    """
    UTF_8 encoding for barcodes. This is only supported for barcode type
    qrCode.
    """
