from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


BaseUser = declarative_base()

class UserData(BaseUser):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)