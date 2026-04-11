from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from random import choice
from utils.object_detection import image_processing
import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

upload_dir = "Image/"
os.makedirs(upload_dir, exist_ok=True)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload/")
async def upload(file: UploadFile):
    try:
        filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()

        filepath = os.path.join(upload_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(contents)

        image_processing(filepath) 

        return {"filename": filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/show/")
def display():
    save_path = 'output_images'
    files = os.listdir(save_path)

    if not files:
        raise HTTPException(status_code=404, detail="No images found")

    selected_file = choice(files)
    path = os.path.join(save_path, selected_file)

    return FileResponse(path)