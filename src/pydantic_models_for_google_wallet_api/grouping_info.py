# https://developers.google.com/wallet/reference/rest/v1/GroupingInfo

from typing import Optional

from pydantic import BaseModel


class GroupingInfo(BaseModel):
    sortIndex: Optional[int] = None
    """
    Optional index for sorting the passes when they are grouped with other
    passes. Passes with lower sort index are shown before passes with higher
    sort index. If unspecified, the value is assumed to be INT_MAX. For two
    passes with the same sort index, the sorting behavior is undefined.
    """

    groupingId: Optional[str] = None
    """
    Optional grouping ID for grouping the passes with the same ID visually
    together. Grouping with different types of passes is allowed.
    """
