from fastapi import APIRouter, UploadFile, File, Query
from app.services.pdf_to_image_converter import PDFToImageConverter

router = APIRouter()

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), response_format: str = Query("png", enum=["png", "jpeg"])):
    uploader = PDFToImageConverter(upload_dir="./uploads")
    return await uploader.upload_pdf(file, response_format)