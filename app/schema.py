from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class Loan(BaseModel):
    LoanOffersID: int
    LoanName: str
    Amount:float
    LoanRange:int
    Interest:float
    class Config:
        from_attributes = True

class User(BaseModel):
    Fname: str
    Lname: str
    address: str
    phone: str
    email: str
    DOB: datetime
    Gender:  str
    bank_balance: float
    password: str


class UserCreate(BaseModel):
    email: str
    password: str

class Userinfo(BaseModel):
    Fname: str
    Lname: str
    address: str
    phone: str
    email: str
    DOB: datetime
    Gender:  str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token:str
    token_type:str

class Loanapply(BaseModel):
    Collateral:str
    LoanAmount:float
    Loanrange: int
    purpose:str

class Loanapp(BaseModel):
    Collateral:str
    purpose:str


class Tokendata(BaseModel):
    id: Optional[int] = None