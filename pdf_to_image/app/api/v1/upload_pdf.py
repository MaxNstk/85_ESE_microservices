from fastapi import APIRouter, UploadFile, File
from app.services.pdf_to_image_converter import PDFToImageConverter

router = APIRouter()

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    uploader = PDFToImageConverter(upload_dir="./uploads")
    return await uploader.upload_pdf(file)