# Generic wrapper of a resource returned by the Google Wallet API as a result
# of an API call modifying or creating a sub-resource. See for example:
# https://developers.google.com/wallet/reference/rest/v1/eventticketclass/addmessage#response-body

from pydantic import BaseModel

from ._discovery_meta import discovery_schema


@discovery_schema("*AddMessageResponse")
class ResourceResponse[ResourceType: BaseModel](BaseModel):
    """
    Generic wrapper of a resource returned by the Google Wallet API as a result
    of an API call modifying or creating a sub-resource.
    """

    resource: ResourceType
    """
    The updated resource that had a sub-resource modified or created. For
    example, if the API call was to add a message to an event ticket class,
    this would be the event ticket class that had the message added.
    """


@discovery_schema(
    "SetPassUpdateNoticeResponse",
    "TransitObjectUploadRotatingBarcodeValuesResponse",
)
class EmptyResponse(BaseModel):
    """
    A response with no content. Used for API calls that do not return a
    resource.
    """

    pass
