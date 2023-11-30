from datetime import datetime, timedelta
from typing import List
from fastapi import BackgroundTasks, FastAPI, Depends , HTTPException,status,Response
from . import model,schema,oauth
from .router import auth
from .database import engine, get_db
from sqlalchemy.orm import Session


model.Base.metadata.create_all(bind=engine)
app = FastAPI()
background_task = BackgroundTasks()
app.include_router(auth.router)

def debit_user(db: Session, user_id: int, amount: float):
    user = db.query(model.Customers).filter(model.Customers.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    loans = db.query(model.Loan).filter(model.Loan.customer_id == user_id).all()
    if not loans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active loans for the user")
    total_loan_amount = sum(loan.amount for loan in loans)
    if amount > total_loan_amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Repayment amount exceeds total loan amount")
    for loan in loans:
        loan_repayment = (loan.amount / total_loan_amount) * amount
        loan.amount -= loan_repayment
        user.bank_balance -= loan_repayment
    new_transaction = model.Transaction(
        customer_id=user_id,
        purpose="Loan Repayment",
        amount=-amount,  # Assuming negative amount for repayment
        timestamp=datetime.now(),
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(user)
    return {"message": f"Loan repayment successful. Updated bank balance: {user.bank_balance}"}


@app.get("/")
async def root():
    return {"message": "Hello World"}

#get loan offers
@app.get("/loans", response_model= List[schema.Loan])
def Available_Loans(db: Session =  Depends(get_db)):
    loans = db.query(model.LoanOffer).all()
    return loans

@app.post("/loans/{id}")
def Get_loan(info: schema.Loanapp, id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
    loanoffer = db.query(model.LoanOffer).where(model.LoanOffer.LoanOffersID == id).first()
    if not loanoffer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan does not exist")
    print (current_user.bank_balance)
    new_trans = model.Transaction(loan_id = id, customer_id=current_user.id, purpose = info.purpose, collateral= info.Collateral)
    new_loan = model.Loan(amount = loanoffer.Amount, intrest_rate = loanoffer.Interest, duedate  = datetime.now() + timedelta(days=365*loanoffer.LoanRange),customer_id =current_user.id)
    db.add(new_loan)
    db.add(new_trans)
    current_user.bank_balance = loanoffer.Amount + current_user.bank_balance
    current_user.loan_balance = loanoffer.Amount + current_user.loan_balance
 
    db.commit()
    db.refresh(new_loan)
    db.refresh(new_trans)
    total_repayment = loanoffer.Amount + (loanoffer.Amount * loanoffer.Interest * loanoffer.LoanRange)
    background_task.add_task(debit_user, db, current_user.id, total_repayment,)
    return {"message": f"You are now owing {current_user.loan_balance}"}


@app.post("/getloan")
def Custom_loan(info:schema.Loanapply ,db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
    current_user.bank_balance = info.LoanAmount + current_user.bank_balance
    current_user.loan_balance = info.LoanAmount + current_user.loan_balance
    
    new_loan = model.Loan(amount = info.LoanAmount, intrest_rate = 10, duedate  = datetime.now() + timedelta(days=365*info.Loanrange),customer_id =current_user.id)
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    new_trans = model.Transaction(loan_id = new_loan.id, customer_id=current_user.id, purpose = info.purpose, collateral= info.Collateral)
    db.add(new_trans)
    total_repayment = info.LoanAmount + (info.LoanAmount * 10 * info.Loanrange)
    background_task.add_task(debit_user, db, current_user.id, total_repayment,)
    db.commit()
    return {"message": f"Your loan has been approved. your new bank balance is {current_user.bank_balance}"}

@app.post("/payloans/{id}")
def Get_loan(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
    loans = db.query(model.Loan).where(model.Loan.id == id).first()
    if not loans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan does not exist")
    
    return {"message": f"You are now owing"}
