from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import status
from db import database
from decouple import config

from models import user, RoleType


class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                "sub": user["id"],
                "exp": datetime.utcnow() + timedelta(minutes=120)
            }
            return jwt.encode(payload, config("SECRET_KEY"), algorithm="HS256")
        except Exception as ex:
            # Log the exception
            raise ex


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
            self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(res.credentials, config(
                "SECRET_KEY"), algorithms="HS256")
            user_data = await database.fetch_one(user.select()
                                                 .where(user.c.id == payload["sub"]))
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Token")


oauth2_scheme = CustomHTTPBearer()


def is_complainer(request: Request):
    if not request.state.user["role"] == RoleType.complainer:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")


def is_approver(request: Request):
    if not request.state.user["role"] == RoleType.approver:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")


def is_admin(request: Request):
    if not request.state.user["role"] == RoleType.admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")
