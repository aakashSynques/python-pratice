# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from fastapi import HTTPException, Depends
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from sqlalchemy.orm import Session
# from app.database.db import get_db
# from app.models.master_users import MasterUser
# import hashlib

# # JWT Configuration
# SECRET_KEY = "aakash" 
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# bearer_scheme = HTTPBearer()

# #  Simple SHA256 Hash
# def get_password_hash(password: str):
#     return hashlib.sha256(password.encode()).hexdigest()

# #  Verify Password
# def verify_password(plain_password: str, hashed_password: str):
#     return hashlib.sha256(
#         plain_password.encode()
#     ).hexdigest() == hashed_password


# # Create JWT Token
# def create_access_token(data: dict, expires_delta: timedelta = None):

#     to_encode = data.copy()

#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(
#             minutes=ACCESS_TOKEN_EXPIRE_MINUTES
#         )

#     to_encode.update({"exp": expire})

#     encoded_jwt = jwt.encode(
#         to_encode,
#         SECRET_KEY,
#         algorithm=ALGORITHM
#     )

#     return encoded_jwt


# # Verify Token
# def verify_token(token: str, credentials_exception):

#     try:
#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )

#         email: str = payload.get("sub")

#         if email is None:
#             raise credentials_exception

#         return email

#     except JWTError:
#         raise credentials_exception


# # Get Current User
# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
#     db: Session = Depends(get_db)
# ):

#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     token = credentials.credentials
#     email = verify_token(token, credentials_exception)

#     user = db.query(MasterUser).filter(
#         MasterUser.email == email
#     ).first()

#     if user is None:
#         raise credentials_exception

#     return user



from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.master_users import MasterUser

# JWT Configuration
SECRET_KEY = "aakash"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bearer_scheme = HTTPBearer()


# ✅ Verify Password (Plain Text Only)
def verify_password(plain_password: str, db_password: str):

    if plain_password == db_password:
        return True

    return False


# ✅ Create JWT Token
def create_access_token(data: dict, expires_delta: timedelta = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ✅ Verify Token
def verify_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        return email

    except JWTError:
        raise credentials_exception


# ✅ Get Current User (Protected Routes)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    email = verify_token(
        token,
        credentials_exception
    )

    user = db.query(MasterUser).filter(
        MasterUser.email == email
    ).first()

    if user is None:
        raise credentials_exception

    return user