from typing import Dict

from fastapi import status
from typing import Optional
from fastapi import Request
from fastapi import HTTPException
from fastapi.security import OAuth2

from constants import ACCESS_TOKEN_KEY, AUTHORIZATION_SCHEME

from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param


class OAuth2PasswordBearerWithCookie(OAuth2):
    """This class is used to handle OAuth2 Password Bearer with HTTP-Only Cookie.

    Args:
        OAuth2 (_type_)
    """
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get(ACCESS_TOKEN_KEY)

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != AUTHORIZATION_SCHEME.lower():
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid user",
                    headers={"WWW-Authenticate": AUTHORIZATION_SCHEME},
                )
            else:
                return None
        return param