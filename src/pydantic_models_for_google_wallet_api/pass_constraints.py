# https://developers.google.com/wallet/reference/rest/v1/PassConstraints

from enum import Enum

from pydantic import BaseModel


class ScreenshotEligibility(str, Enum):
    """
    Defines if/how screenshots may be taken of a pass.
    """

    SCREENSHOT_ELIGIBILITY_UNSPECIFIED = "SCREENSHOT_ELIGIBILITY_UNSPECIFIED"
    """
    Default value, same as ELIGIBLE.
    """

    ELIGIBLE = "ELIGIBLE"
    """
    Default behavior for all existing Passes if ScreenshotEligibility is not
    set. Allows screenshots to be taken on Android devices.
    """

    INELIGIBLE = "INELIGIBLE"
    """
    Disallows screenshots to be taken on Android devices. Note that older
    versions of Wallet may still allow screenshots to be taken.
    """


class NfcConstraint(str, Enum):
    """
    Defines possible NFC constraints for the pass.
    """

    NFC_CONSTRAINT_UNSPECIFIED = "NFC_CONSTRAINT_UNSPECIFIED"
    """
    Default value, no specified constraint.
    """

    BLOCK_PAYMENT = "BLOCK_PAYMENT"
    """
    Payment cards will not be conveyed while the pass is open.
    """

    BLOCK_CLOSED_LOOP_TRANSIT = "BLOCK_CLOSED_LOOP_TRANSIT"
    """
    Closed loop transit cards will not be conveyed while the pass is open.
    """


class PassConstraints(BaseModel):
    """
    Container for any constraints that may be placed on passes.
    """

    screenshotEligibility: ScreenshotEligibility = (
        ScreenshotEligibility.SCREENSHOT_ELIGIBILITY_UNSPECIFIED
    )
    """
    The screenshot eligibility for the pass.
    """

    nfcConstraint: list[NfcConstraint] = [
        NfcConstraint.NFC_CONSTRAINT_UNSPECIFIED,
    ]
    """
    The NFC constraints for the pass.
    """
