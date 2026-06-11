from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM")])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = await User.find_one(User.email == email)
    if user is None:
        raise credentials_exception
    return user
