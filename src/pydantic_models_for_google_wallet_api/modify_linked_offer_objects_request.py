# https://developers.google.com/wallet/reference/rest/v1/ModifyLinkedOfferObjectsRequest

from pydantic import BaseModel, Field


class ModifyLinkedOfferObjects(BaseModel):
    addLinkedOfferObjectIds: list[str] = Field(default_factory=list)
    """
    The linked offer object ids to add to the object.
    """

    removeLinkedOfferObjectIds: list[str] = Field(default_factory=list)
    """
    The linked offer object ids to remove from the object.
    """


class ModifyLinkedOfferObjectsRequest(BaseModel):
    linkedOfferObjectIds: ModifyLinkedOfferObjects
    """
    The linked offer object ids to add or remove from the object.
    """
