# https://developers.google.com/wallet/reference/rest/v1/AddMessageRequest

from pydantic import BaseModel

from .message import Message


class AddMessageRequest(BaseModel):
    """
    Resource used when the AddMessage endpoints are called
    """

    message: Message
