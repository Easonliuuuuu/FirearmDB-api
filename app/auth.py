from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from slowapi.util import get_remote_address
from app import models, schemas
from app.config import settings
from app.database import get_db
from app.context import _request_ctx_var # Import from the new context file
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def try_get_current_user(request: Request, db: Session = Depends(get_db)) -> models.User | None:
    """
    Tries to get the current user from the token in the request headers.
    Returns the user object if successful, otherwise returns None.
    Does not raise an exception for invalid/missing credentials.
    """
    token = request.headers.get("Authorization")
    if token:
        try:
            # Assuming the token is prefixed with "Bearer "
            token = token.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email:
                return db.query(models.User).filter(models.User.email == email).first()
        except (JWTError, IndexError):
            # This handles cases where the token is invalid or not in the "Bearer <token>" format
            return None
    return None

def dynamic_key_func() -> str:
    request = _request_ctx_var.get()
    if request and hasattr(request.state, "user") and request.state.user:
        print(f"Rate limiting based on user: {request.state.user.email}")
        return request.state.user.email
    
    if request:
        print("Rate limiting based on IP address")
        return get_remote_address(request)
    
    return "anonymous"


'''
def rate_limit_dependency(request: Request) -> str:
    """
    Returns a rate limit string based on the user's authentication status,
    which is expected to be in request.state.
    """
    if hasattr(request.state, "user") and request.state.user:
        print(f"Applying authenticated rate limit for user: {request.state.user.email}")
        return "5/minute"
    else:
        print("Applying anonymous rate limit based on IP address")
        return "2/minute"

'''

def get_rate_limit() -> str:
    request = _request_ctx_var.get()
    if request and hasattr(request.state, "user") and request.state.user:
        print(f"Applying authenticated rate limit for user: {request.state.user.email}")
        return "5/minute"
    
    print("Applying anonymous rate limit based on IP address")
    return "2/minute"

def is_user_exempt(request: Request) -> bool:
    """
    Returns True if the user is exempt from rate limiting, False otherwise.
    """
    # Add your exemption logic here. For example, you could check if the
    # user has a specific role or is in a whitelist.
    # For now, we'll just return False so no one is exempt.
    return False
