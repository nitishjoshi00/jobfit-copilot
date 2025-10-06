from fastapi import Header, HTTPException, status, Depends
from typing import Optional
import jwt
import os

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALG = os.getenv("JWT_ALG", "HS256")

def parse_user_id(authorization: Optional[str] = Header(None), x_user_id: Optional[str] = Header(None)):
    if authorization:
        try:
            scheme, token = authorization.split(" ")
            if scheme.lower() != "bearer":
                raise ValueError("Invalid auth scheme")
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
            user_id = payload.get("sub")
            if not user_id:
                raise ValueError("Missing 'sub' in token")
            return user_id
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}")
    if x_user_id:
        return x_user_id
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No credentials provided")

UserIdDep = Depends(parse_user_id)
