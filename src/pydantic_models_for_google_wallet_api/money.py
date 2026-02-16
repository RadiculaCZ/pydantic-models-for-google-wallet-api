# https://developers.google.com/wallet/reference/rest/v1/Money

from typing import Annotated, Literal

from pydantic import BaseModel, Field
from typing_extensions import deprecated


class Money(BaseModel):
    kind: Annotated[
        Literal["walletobjects#money"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#money"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#money"`.
    """

    micros: int
    """
    The unit of money amount in micros. For example, $1 USD would be
    represented as 1000000 micros.
    """

    currencyCode: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern=r"^([A-Z]{3}|[0-9]{3})$",  # ISO 4217 currency code.
    )
    """
    The currency code, such as "USD" or "EUR."
    """
