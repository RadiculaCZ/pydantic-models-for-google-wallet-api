# Generic resource listing returned by the Google Wallet API See for example:
# https://developers.google.com/wallet/reference/rest/v1/eventticketclass/list#response-body

from pydantic import BaseModel

from .pagination import Pagination


class ResourceListing[ResourceType: BaseModel](BaseModel):
    """
    Generic listing of resources returned by the Google Wallet API.
    """

    resources: list[ResourceType]
    """
    Resources corresponding to the list request.
    """


class ResourcePaginatedListing[ResourceType: BaseModel](BaseModel):
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
