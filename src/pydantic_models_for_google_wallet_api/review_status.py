# https://developers.google.com/wallet/reference/rest/v1/ReviewStatus

from enum import Enum


class ReviewStatus(str, Enum):
    REVIEW_STATUS_UNSPECIFIED = "REVIEW_STATUS_UNSPECIFIED"

    UNDER_REVIEW = "UNDER_REVIEW"

    underReview = "underReview"
    """
    Legacy alias for `UNDER_REVIEW`. Deprecated.
    """

    APPROVED = "APPROVED"

    approved = "approved"
    """
    Legacy alias for `APPROVED`. Deprecated.
    """

    REJECTED = "REJECTED"

    rejected = "rejected"
    """
    Legacy alias for `REJECTED`. Deprecated.
    """

    DRAFT = "DRAFT"

    draft = "draft"
    """
    Legacy alias for `DRAFT`. Deprecated.
    """
