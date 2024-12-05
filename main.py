import io
import os
from datetime import datetime
from functools import lru_cache

import uvicorn
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.responses import FileResponse
from starlette import status
from PIL import Image


app = FastAPI(docs_url="/docs")

UPLOAD_DIR = "./upload_files"
MAX_FILE_SIZE = 1.5 * 1024 * 1024       # 10 Gb
ALLOWED_FILE_TYPES = ["image/jpeg", "image/png"]


@app.post("/file/upload")
async def upload_files(file: UploadFile = File(..., description="upload any files")):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path_file = os.path.join(UPLOAD_DIR, file.filename)

    content_file = await file.read()
    with open(path_file, "wb") as buffer:
        buffer.write(content_file)

    with open(path_file, "a") as buffer:
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        buffer.write(f"file uploaded on: {current_date}")

    return {"file": file, "about": f'{file.filename} uploaded'}


@app.get("/file/download")
def download_file(filename: str = Query(..., description="Enter filename for downloads")):
    file_path = os.path.join(UPLOAD_DIR, filename)
    return FileResponse(path=file_path,
                        filename='New file from service.txt',
                        media_type='multipart/form-data')


def resize_image(image_data: bytes, max_size: tuple = (80, 60)) -> bytes:
    with Image.open(io.BytesIO(image_data)) as img:
        img.thumbnail(max_size)
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format=img.format)
        return img_byte_array.getvalue()


async def process_image(file_path: str):
    with open(file_path, "rb") as file:
        resized_image = resize_image(file.read())
    with open(file_path, "wb") as file:
        file.write(resized_image)


@app.post("/image/upload")
async def upload_image(files: list[UploadFile] = File(..., description="upload only images")):
    for file in files:
        if file.size > MAX_FILE_SIZE:
            raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="file is too large")
        if file.content_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Unknown file type")

        image_content: bytes = await file.read()
        resized_image = resize_image(image_content)
        print(resized_image)


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
