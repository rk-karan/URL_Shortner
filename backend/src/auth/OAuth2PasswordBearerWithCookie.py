from typing import Dict, Optional
from fastapi.security import OAuth2
from fastapi import status, Request, HTTPException
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from src.constants import ACCESS_TOKEN_KEY, AUTHORIZATION_SCHEME, INVALID_USER_MESSAGE

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
                    detail=INVALID_USER_MESSAGE,
                    headers={"WWW-Authenticate": AUTHORIZATION_SCHEME},
                )
            else:
                return None
        return param