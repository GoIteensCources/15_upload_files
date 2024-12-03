import os
import uvicorn
from fastapi import FastAPI, UploadFile, File


app = FastAPI(docs_url="/docs")

UPLOAD_DIR = "./upload_files"


@app.post("/file/upload")
async def upload_image(file: UploadFile = File(..., description="upload any files")):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path_file = os.path.join(UPLOAD_DIR, file.filename)

    content_file = await file.read()
    with open(path_file, "wb") as buffer:
        buffer.write(content_file)

    return {"file": file, "about": f'{file.filename} uploaded'}


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
