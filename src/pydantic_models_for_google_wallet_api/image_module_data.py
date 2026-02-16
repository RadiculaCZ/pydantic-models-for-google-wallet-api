# https://developers.google.com/wallet/reference/rest/v1/ImageModuleData

from pydantic import BaseModel

from .image import Image


class ImageModuleData(BaseModel):
    mainImage: Image
    """
    A 100% width image.
    """

    id: str
    """
    The ID associated with an image module. This field is here to enable ease
    of management of image modules.
    """
