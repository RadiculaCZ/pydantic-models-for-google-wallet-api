# Generic resource listing returned by the Google Wallet API See for example:
# https://developers.google.com/wallet/reference/rest/v1/eventticketclass/list#response-body

from pydantic import BaseModel

from ._discovery_meta import discovery_schema
from .pagination import Pagination


@discovery_schema("*ListResponse")
class PaginatedResourceListing[ResourceType: BaseModel](BaseModel):
    """
    Generic paginated listing of resources returned by the Google Wallet API.
    """

    resources: list[ResourceType]
    """
    Resources corresponding to the list request.
    """

    pagination: Pagination
    """
    Pagination of the response.
    """
