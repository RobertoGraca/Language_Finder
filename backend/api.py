from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from language_finder import get_language
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/lang")
async def get_lang_from_file(file_upload: UploadFile):
    data = await file_upload.read()
    with open(file_upload.filename, 'wb') as f:
        f.write(data)
    file_lang = get_language(file_upload.filename)
    os.remove(file_upload.filename)
    return {'lang': file_lang}
    