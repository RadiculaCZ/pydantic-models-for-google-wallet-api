# https://developers.google.com/wallet/reference/rest/v1/Review

from pydantic import BaseModel


class Review(BaseModel):
    comments: str
