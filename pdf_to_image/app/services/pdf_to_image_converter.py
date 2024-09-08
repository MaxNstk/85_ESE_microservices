import os
import shutil
from fastapi import UploadFile, HTTPException
import fitz
from io import BytesIO
from fastapi.responses import StreamingResponse
from PIL import Image

class PDFToImageConverter:
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    # Manipula o upload do arquivo PDF, converte a primeira página para imagem e retorna a imagem como resposta.
    async def upload_pdf(self, file: UploadFile):

        # Verificando se o arquivo enviado é um PDF
        if not self.is_pdf(file):
            raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF")

        file_location = self.save_file(file)
        try:
            image = self.convert_first_page_to_image(file_location)
            return self.create_image_response(image)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao converter PDF: {str(e)}")

    def is_pdf(self, file: UploadFile) -> bool:
        return file.content_type == "application/pdf"

    def save_file(self, file: UploadFile) -> str:
        file_location = f"{self.upload_dir}/{file.filename}" # Diretório temporário para que posteriormente seja convertido
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_location

    def convert_first_page_to_image(self, file_location: str) -> Image:
        pixelmap = fitz.open(file_location).load_page(0).get_pixmap() # Buscando pixelmap apenas da primeira página do PDF 
        return Image.frombytes("RGB", [pixelmap.width, pixelmap.height], pixelmap.samples)

    # Realizando conversão da imagem para um retorno HTTPS.
    def create_image_response(self, image: Image) -> StreamingResponse:
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return StreamingResponse(img_byte_arr, media_type="image/png")
