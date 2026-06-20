# https://developers.google.com/wallet/reference/rest/v1/jwt

from typing import Optional

from pydantic import BaseModel

from .event_ticket_class import EventTicketClass
from .event_ticket_object import EventTicketObject
from .flight_class import FlightClass
from .flight_object import FlightObject
from .generic_class import GenericClass
from .generic_object import GenericObject
from .gift_card_class import GiftCardClass
from .gift_card_object import GiftCardObject
from .loyalty_class import LoyaltyClass
from .loyalty_object import LoyaltyObject
from .offer_class import OfferClass
from .offer_object import OfferObject
from .transit_class import TransitClass
from .transit_object import TransitObject


class JwtResource(BaseModel):
    jwt: Optional[str] = None
    """
    A string representing a JWT of the format described at
    https://developers.google.com/wallet/reference/rest/v1/Jwt

    See the `JWT` class.
    """


class Resources(BaseModel):
    eventTicketClasses: Optional[list[EventTicketClass]] = None
    """
    A list of event ticket classes.
    """

    eventTicketObjects: Optional[list[EventTicketObject]] = None
    """
    A list of event ticket objects.
    """

    flightClasses: Optional[list[FlightClass]] = None
    """
    A list of flight classes.
    """

    flightObjects: Optional[list[FlightObject]] = None
    """
    A list of flight objects.
    """

    giftCardClasses: Optional[list[GiftCardClass]] = None
    """
    A list of gift card classes.
    """

    giftCardObjects: Optional[list[GiftCardObject]] = None
    """
    A list of gift card objects.
    """

    loyaltyClasses: Optional[list[LoyaltyClass]] = None
    """
    A list of loyalty classes.
    """

    loyaltyObjects: Optional[list[LoyaltyObject]] = None
    """
    A list of loyalty objects.
    """

    offerClasses: Optional[list[OfferClass]] = None
    """
    A list of offer classes.
    """

    offerObjects: Optional[list[OfferObject]] = None
    """
    A list of offer objects.
    """

    transitClasses: Optional[list[TransitClass]] = None
    """
    A list of transit classes.
    """

    transitObjects: Optional[list[TransitObject]] = None
    """
    A list of transit objects.
    """

    genericClasses: Optional[list[GenericClass]] = None
    """
    A list of generic classes.
    """

    genericObjects: Optional[list[GenericObject]] = None
    """
    A list of generic objects.
    """


class JwtResourceInsertResponse(BaseModel):
    """
    Response body for the insert operation on the JWT resource.
    """

    saveUri: str
    """
    A URI that, when opened, will allow the end user to save the object(s)
    identified in the JWT to their Google account.
    """

    resources: Resources
    """
    Data that corresponds to the ids of the provided classes and objects in the
    JWT. resources will only include the non-empty arrays (i.e. if the JWT only
    includes eventTicketObjects, then that is the only field that will be
    present in resources).
    """
