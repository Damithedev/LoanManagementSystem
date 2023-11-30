from fastapi import APIRouter, FastAPI, responses,Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schema,utils,model,oauth

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/signup", response_model=schema.Userinfo)
def Create_User(user:schema.User ,db: Session =  Depends(get_db)):
    hashed_pwd= utils.hash(user.password)
    user.password = hashed_pwd
    new_user = model.Customers(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user

@router.post("/login", response_model=schema.Token)
def Login_User(usercred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user =  db.query(model.Customers).filter(model.Customers.email == usercred.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    if not utils.verify(usercred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "invalid credentials")
    access_token = oauth.create_acces_token(data= {"user_id": user.id})
    return schema.Token(access_token=access_token, token_type="bearer")