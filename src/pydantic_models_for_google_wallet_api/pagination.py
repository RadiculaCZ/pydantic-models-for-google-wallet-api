# https://developers.google.com/wallet/reference/rest/v1/Pagination

from typing import Annotated, Literal

from pydantic import BaseModel
from typing_extensions import deprecated


class Pagination(BaseModel):
    kind: Annotated[
        Literal["walletobjects#pagination"],
        deprecated("This item is deprecated!"),
    ] = "walletobjects#pagination"
    """
    Identifies what kind of resource this is. Value: the fixed string
    `"walletobjects#pagination"`.
    """

    resultsPerPage: int
    """
    Number of results returned in this page.
    """

    nextPageToken: str
    """
    Page token to send to fetch the next page.
    """
