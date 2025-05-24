import json
from sqlalchemy.orm import Session
from models.scraped_data import ScrapedData
from datetime import datetime

def salvar_scraping(db: Session, url: str, categoria: str, titulos: list, paragrafos: list, dados: list, ano: int = None):
    dados_json = json.dumps(dados, ensure_ascii=False)
    registro = db.query(ScrapedData).filter_by(url=url, ano=ano).first()

    if registro:
        registro.titulos = json.dumps(titulos, ensure_ascii=False)
        registro.paragrafos = json.dumps(paragrafos, ensure_ascii=False)
        registro.dados_json = dados_json
        registro.atualizado_em = datetime.utcnow()
    else:
        registro = ScrapedData(
            url=url,
            ano=ano,
            categoria=categoria,
            titulos=json.dumps(titulos, ensure_ascii=False),
            paragrafos=json.dumps(paragrafos, ensure_ascii=False),
            dados_json=dados_json
        )
        db.add(registro)

    db.commit()

