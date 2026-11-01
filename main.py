from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import func,Column,Integer,String,Float,Date,ForeignKey
from sqlalchemy.orm import Session
import models, schemas, auth
from database import engine, get_db,Base
from models import expense
from datetime import date

models.Base.metadata.create_all(bind=engine)  # creates MySQL tables
app = FastAPI(title="Expense Tracker API")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", include_in_schema=False)
def home():
    return FileResponse("static/index.html")
@app.post("/register", status_code=201)
def register(data: schemas.usercreate, db: Session = Depends(get_db)):
    if db.query(models.user).filter_by(username=data.username).first():
        raise HTTPException(400, "Username already exists")
    db.add(models.user(username=data.username, password=auth.hashed_password(data.password)))
    db.commit()
    return {"message": "User registered"}
@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.user).filter_by(username=form.username).first()
    if not user or not auth.verify_password(form.password, user.password):
        raise HTTPException(401, "Wrong username or password")
    return {"access_token": auth.create_token(user.username), "token_type": "bearer"}
def get_own_expense(expense_id: int, db: Session, user: models.user):
    exp = db.query(models.expense).filter_by(id=expense_id, user_id=user.id).first()
    if not exp:
        raise HTTPException(404, "Expense not found")
    return exp
@app.post("/expenses", response_model=schemas.expenseout, status_code=201)
def add_expense(data: schemas.expensecreate, db: Session = Depends(get_db),
                user: models.user = Depends(auth.get_user)):
    exp = models.expense(
        title=data.title,
        amount=data.amount,
        category=data.category,
        date=data.date or date.today(),
        user_id=user.id,

    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp
@app.get("/expenses", response_model=list[schemas.expenseout])
def list_expenses(db: Session = Depends(get_db), user: models.user = Depends(auth.get_user)):
    return db.query(models.expense).filter(models.expense.user_id==user.id).all()
@app.put("/expenses/{expense_id}", response_model=schemas.expenseout)
def update_expense(expense_id: int, data: schemas.expensecreate, db: Session = Depends(get_db),
                   user: models.user = Depends(auth.get_user)):
    exp = get_own_expense(expense_id, db, user)
    for key, value in data.model_dump().items():
        setattr(exp, key, value)
    db.commit()
    db.refresh(exp)
    return exp
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db),
                   user: models.user = Depends(auth.get_user)):
    db.delete(get_own_expense(expense_id, db, user))
    db.commit()
    return {"message": "Deleted"}
@app.get("/summary")
def summary(db: Session = Depends(get_db), user: models.user = Depends(auth.get_user)):
    rows = (db.query(models.expense.category, func.sum(models.expense.amount))
            .filter_by(user_id=user.id).group_by(models.expense.category).all())
    return {cat: total for cat, total in rows}
@app.get("/report/monthly")
def monthly_report(year: int, month: int, db: Session = Depends(get_db),
                   user: models.user = Depends(auth.get_user)):
    rows = db.query(models.expense).filter(
        models.expense.user_id == user.id,
        func.year(models.expense.date) == year,
        func.month(models.expense.date) == month).all()
    by_category = {}
    for e in rows:
        by_category[e.category] = by_category.get(e.category, 0) + e.amount
    top = max(rows, key=lambda e: e.amount, default=None)
    return {"year": year, "month": month, "count": len(rows),
            "total": sum(e.amount for e in rows), "by_category": by_category,
            "highest_expense": {"title": top.title, "amount": top.amount} if top else None}