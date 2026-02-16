# https://developers.google.com/wallet/reference/rest/v1/LinksModuleData

from pydantic import BaseModel

from .uri import Uri


class LinksModuleData(BaseModel):
    uris: list[Uri]
    """
    The list of URIs.
    """
