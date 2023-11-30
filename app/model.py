from sqlalchemy import DATETIME, TIMESTAMP, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from .database import Base

class Customers(Base):
    __tablename__ = "Customers"

    id = Column(Integer, primary_key=True, nullable=False)
    Fname = Column(String(255), nullable=False)
    Lname = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    phone =  Column(String(11), nullable= False)
    email = Column(String(70), nullable=False, unique=True)
    DOB = Column(Date, nullable=False)
    Gender = Column(String(7), nullable=False)
    loan_balance =  Column(Float, nullable=False, default=0.0)
    bank_balance = Column(Float, nullable=False, default= 0.0)
    password = Column(String(300), nullable=False)

class Loan(Base):
    __tablename__ = "Loans"

    id = Column(Integer, primary_key=True, nullable=False)
    amount =  Column(Float, nullable=False)
    intrest_rate =  Column(Float, nullable=False)
    appdate  =  Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('NOW()'))
    duedate  =  Column(DATETIME, nullable=False)
    customer_id = Column(Integer, ForeignKey("Customers.id", ondelete= "CASCADE"), nullable=False)


class Transaction(Base):
    __tablename__ =  "transactions"

    id = Column(Integer, primary_key=True, nullable=False)
    DOT = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('NOW()'))
    purpose = Column(String(255), nullable=False)
    collateral =  Column(String(255), nullable=False)
    customer_id = Column(Integer, ForeignKey("Customers.id", ondelete= "CASCADE"), nullable=False)
    loan_id = Column(Integer, ForeignKey("Loans.id", ondelete= "CASCADE"), nullable=False)


class Payinfo(Base):
    __tablename__ = "Payinfo"
    
    id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("Customers.id", ondelete= "CASCADE"), nullable=False)
    loan_id = Column(Integer, ForeignKey("Loans.id", ondelete= "CASCADE"), nullable=False)
    amount_pay = Column(Float, nullable=False)
    DOp = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('NOW()'))


class LoanOffer(Base):
    __tablename__ = 'loan_offers'
  
    LoanOffersID = Column(Integer, primary_key=True, nullable=False)
    LoanName = Column(String(255), nullable=False)
    Amount = Column(Float, nullable=False)
    LoanRange = Column(Integer, nullable=False)
    Interest = Column(Float, nullable=False)

