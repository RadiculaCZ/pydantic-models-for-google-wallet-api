# https://developers.google.com/wallet/reference/rest/v1/Jwt

from typing import Optional

from pydantic import BaseModel


class JwtPayload(BaseModel):
    eventTicketClasses: Optional[list] = None
    """
    Event Ticket Class to save.
    """

    eventTicketObjects: Optional[list] = None
    """
    Event Ticket Object to save.
    """

    flightClasses: Optional[list] = None
    """
    Flight Class to save.
    """

    flightObjects: Optional[list] = None
    """
    Flight Object to save.
    """

    giftCardClasses: Optional[list] = None
    """
    Gift Card Class to save.
    """

    giftCardObjects: Optional[list] = None
    """
    Gift Card Object to save.
    """

    loyaltyClasses: Optional[list] = None
    """
    Loyalty Class to save.
    """

    loyaltyObjects: Optional[list] = None
    """
    Loyalty Object to save.
    """

    offerClasses: Optional[list] = None
    """
    Offer Class to save.
    """

    offerObjects: Optional[list] = None
    """
    Offer Object to save.
    """

    transitClasses: Optional[list] = None
    """
    Transit Class to save.
    """

    transitObjects: Optional[list] = None
    """
    Transit Object to save.
    """


class JWT(BaseModel):
    iss: str
    """
    Your Google Cloud service account generated email address.
    """

    aud: str
    """
    Audience. The audience for Google Wallet API Objects will always be
    `google`.
    """

    typ: str
    """
    Type of JWT. The audience for Google Wallet API Objects will always be
    `savetowallet`.
    """

    iat: str
    """
    Issued at time in seconds since epoch.
    """

    payload: JwtPayload
    """
    Payload object.
    """

    origins: list[str]
    """
    Array of domains to approve for JWT saving functionality. The Google Wallet
    API button will not render when the `origins` field is not defined. You
    could potentially get a "Load denied by X-Frame-Options" or "Refused to
    display" messages in the browser console when the origins field is not
    defined.
    """


GoogleWalletApiJWT = JWT
