from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone
from db import get_db, UserDB


SECRET_KEY = "my-super-secret-key"
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)



def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update( {
            "exp":expire
        })
    
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Invalid authentication credentials")

    try:

        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(UserDB).filter(UserDB.username == username).first()

    if user is None:
        raise credentials_exception

    return user


def admin_required(current_user: UserDB = Depends(get_current_user)):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user