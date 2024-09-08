from fastapi import FastAPI
from app.api.v1.upload_pdf import router as upload_router

app = FastAPI()
app.include_router(upload_router, prefix="/api/v1")