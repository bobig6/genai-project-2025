from fastapi import FastAPI
from app.api import predict, admin

app = FastAPI()

app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])