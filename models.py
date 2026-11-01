from database import Base
from sqlalchemy import Column,Integer,String,Float,Date,ForeignKey
from datetime import date


class user(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    password=Column(String(255))
    username=Column(String(100))

class expense(Base):
    __tablename__="expenses"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(50),nullable=False)
    amount=Column(Float(50),nullable=False)
    category=Column(String(50))
    date=Column(Date,default=date.today,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"))