# https://developers.google.com/wallet/reference/rest/v1/walletobjects.v1.privateContent

from pydantic import BaseModel


class SetPassUpdateNoticeRequest(BaseModel):
    """
    Request to send a private pass update notice information to Google, so that
    devices can then fetch the notice prompting the user to update a pass.
    """

    externalPassId: str
    """
    Required. A fully qualified identifier of the pass that the issuer wants to
    notify the pass holder(s) about. Formatted as .
    """

    updatedPassJwtSignature: str
    """
    Required. The JWT signature of the updated pass that the issuer wants to
    notify Google about. Only devices that report a different JWT signature
    than this JWT signature will receive the update notification.
    """

    updateUri: str
    """
    Required. The issuer endpoint URI the pass holder needs to follow in order
    to receive an updated pass JWT. It can not contain any sensitive
    information. The endpoint needs to authenticate the user before giving the
    user the updated JWT. Example update URI
    https://someissuer.com/update/passId=someExternalPassId
    """
