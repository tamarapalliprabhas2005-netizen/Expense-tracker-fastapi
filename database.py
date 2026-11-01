from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine
Database_url="mysql+pymysql://root:prabash123@localhost:3306/expense_db"
engine=create_engine(Database_url)
sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()