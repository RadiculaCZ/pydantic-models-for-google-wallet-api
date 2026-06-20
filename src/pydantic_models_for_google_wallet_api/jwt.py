# https://developers.google.com/wallet/reference/rest/v1/Jwt

from typing import Optional

from pydantic import BaseModel

from .event_ticket_class import EventTicketClass
from .event_ticket_object import EventTicketObject
from .flight_class import FlightClass
from .flight_object import FlightObject
from .gift_card_class import GiftCardClass
from .gift_card_object import GiftCardObject
from .loyalty_class import LoyaltyClass
from .loyalty_object import LoyaltyObject
from .offer_class import OfferClass
from .offer_object import OfferObject
from .transit_class import TransitClass
from .transit_object import TransitObject


class JwtPayload(BaseModel):
    eventTicketClasses: Optional[list[EventTicketClass]] = None
    """
    Event Ticket Class to save.
    """

    eventTicketObjects: Optional[list[EventTicketObject]] = None
    """
    Event Ticket Object to save.
    """

    flightClasses: Optional[list[FlightClass]] = None
    """
    Flight Class to save.
    """

    flightObjects: Optional[list[FlightObject]] = None
    """
    Flight Object to save.
    """

    giftCardClasses: Optional[list[GiftCardClass]] = None
    """
    Gift Card Class to save.
    """

    giftCardObjects: Optional[list[GiftCardObject]] = None
    """
    Gift Card Object to save.
    """

    loyaltyClasses: Optional[list[LoyaltyClass]] = None
    """
    Loyalty Class to save.
    """

    loyaltyObjects: Optional[list[LoyaltyObject]] = None
    """
    Loyalty Object to save.
    """

    offerClasses: Optional[list[OfferClass]] = None
    """
    Offer Class to save.
    """

    offerObjects: Optional[list[OfferObject]] = None
    """
    Offer Object to save.
    """

    transitClasses: Optional[list[TransitClass]] = None
    """
    Transit Class to save.
    """

    transitObjects: Optional[list[TransitObject]] = None
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
