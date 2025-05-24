from database import engine
from models.scraped_data import Base

Base.metadata.create_all(bind=engine)