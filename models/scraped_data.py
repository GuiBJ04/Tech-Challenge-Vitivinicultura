# models/scraped_data.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ScrapedData(Base):
    __tablename__ = "scraped_data"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), unique=True, nullable=False)
    ano = Column(Integer, nullable=True)
    categoria = Column(String(100))
    titulos = Column(Text)
    paragrafos = Column(Text)
    dados_json = Column(Text)  # aqui vira json.dumps(tabela)
    atualizado_em = Column(DateTime, default=datetime.utcnow)
