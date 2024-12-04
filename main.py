import os
from datetime import datetime
from functools import lru_cache

import uvicorn
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse


app = FastAPI(docs_url="/docs")

UPLOAD_DIR = "./upload_files"


@app.post("/file/upload")
async def upload_image(file: UploadFile = File(..., description="upload any files")):
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
@lru_cache
def download_file(filename: str = Query(..., description="Enter filename for downloads")):
    file_path = os.path.join(UPLOAD_DIR, filename)
    return FileResponse(path=file_path,
                        filename='New file from service.txt',
                        media_type='multipart/form-data')


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
