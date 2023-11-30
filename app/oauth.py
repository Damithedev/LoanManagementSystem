from fastapi import Depends,status,HTTPException
from jose import JWTError, jwt
import jose
from datetime import datetime, timedelta
from . import schema,model,database
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_acces_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() +timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_acces_token(token: str, credential_exception):
    try:
        payload= jwt.decode(token, SECRET_KEY, [ALGORITHM] )
        id = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schema.Tokendata(id=id)
    except JWTError: 
        raise credential_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WW-Authenticate": "Bearer"})
    token = verify_acces_token(token, credential_exception)
    user=db.query(model.Customers).filter(model.Customers.id == token.id).first()
    return user