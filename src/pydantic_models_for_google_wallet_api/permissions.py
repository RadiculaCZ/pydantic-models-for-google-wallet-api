# https://developers.google.com/wallet/reference/rest/v1/permissions

from enum import Enum

from pydantic import BaseModel, Field


class Role(str, Enum):
    ROLE_UNSPECIFIED = "ROLE_UNSPECIFIED"

    OWNER = "OWNER"

    owner = "owner"
    """
    Legacy alias for `OWNER`. Deprecated.
    """

    READER = "READER"

    reader = "reader"
    """
    Legacy alias for `READER`. Deprecated.
    """

    WRITER = "WRITER"

    writer = "writer"
    """
    Legacy alias for `WRITER`. Deprecated.
    """


class Permission(BaseModel):
    emailAddress: str
    """
    The email address of the user, group, or service account to which this permission refers to.
    """

    role: Role
    """
    The role granted by this permission.
    """


class Permissions(BaseModel):
    issuerId: str
    """
    int64 format

    ID of the issuer the list of permissions refer to.
    """

    permissions: list[Permission] = Field(default_factory=list)
    """
    The complete list of permissions for the issuer account.
    """
