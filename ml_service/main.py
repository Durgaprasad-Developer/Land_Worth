from fastapi import FastAPI
from ml_service.api.price import router as price_router

app = FastAPI()

app.include_router(price_router)
