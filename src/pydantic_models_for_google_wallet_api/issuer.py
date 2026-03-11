# https://developers.google.com/wallet/reference/rest/v1/issuer

from typing import Optional

from pydantic import BaseModel, Field

from .callback_options import CallbackOptions


class IssuerContactInfo(BaseModel):
    name: Optional[str] = None
    """
    The primary contact name.
    """

    phone: Optional[str] = None
    """
    The primary contact phone number.
    """

    email: Optional[str] = None
    """
    The primary contact email address.
    """

    alertsEmails: list[str] = Field(default_factory=list)
    """
    Email addresses which will receive alerts.
    """


class AuthenticationKey(BaseModel):
    id: Optional[int] = None
    """
    Available only to Smart Tap enabled partners. Contact support for
    additional guidance.
    """

    publicKeyPem: Optional[str] = None
    """
    Available only to Smart Tap enabled partners. Contact support for
    additional guidance.
    """


class SmartTapMerchantData(BaseModel):
    smartTapMerchantId: Optional[str] = None
    """
    int64 format

    Available only to Smart Tap enabled partners. Contact support for
    additional guidance.
    """

    authenticationKeys: list[AuthenticationKey] = Field(default_factory=list)
    """
    Available only to Smart Tap enabled partners. Contact support for
    additional guidance.
    """


class Issuer(BaseModel):
    issuerId: Optional[str] = None
    """
    int64 format

    The unique identifier for an issuer account. This is automatically
    generated when the issuer is inserted.
    """

    name: Optional[str] = None
    """
    The account name of the issuer.
    """

    contactInfo: Optional[IssuerContactInfo] = None
    """
    Issuer contact information.
    """

    homepageUrl: Optional[str] = None
    """
    URL for the issuer's home page.
    """

    smartTapMerchantData: Optional[SmartTapMerchantData] = None
    """
    Available only to Smart Tap enabled partners. Contact support for
    additional guidance.
    """

    callbackOptions: Optional[CallbackOptions] = None
    """
    Allows the issuer to provide their callback settings.
    """
