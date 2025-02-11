import shutil

from fastapi import APIRouter, File, UploadFile
from .predict import load_model

import os


router = APIRouter()

@router.post("/")
async def upload_model(file: UploadFile = File(...)):

    # create the /models directory if it does not exist
    if not os.path.exists("models"):
        os.makedirs("models")

    # save the model file in the /models directory
    with open(f"models/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # load the model
    load_model(f"models/{file.filename}")

    return {"message": "Model uploaded successfully"}

