from database import engine, dbCreation
from models.scraped_data import Base
from models.user import BaseUser

Base.metadata.create_all(bind=engine)

BaseUser.metadata.create_all(bind=dbCreation)