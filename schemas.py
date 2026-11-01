from typing import Optional
from pydantic import BaseModel
import datetime

class usercreate(BaseModel):
    username:str
    password:str
class expensecreate(BaseModel):
    title:str
    amount:float
    category:str ="general"
    date:Optional[datetime.date]=None
class expenseout(expensecreate):
    id:int
    date:datetime.date
    class config:
        from_attributes=True