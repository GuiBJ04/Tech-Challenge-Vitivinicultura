from fastapi import FastAPI
from api.auth.auth import router as auth_router
from api.scraped_data import router as scraped_data_router

app = FastAPI(
    title="API Vitivinicultura", 
    description="API pública baseada em dados da Embrapa.",
    version="1.0"
)

app.include_router(auth_router)
app.include_router(scraped_data_router)