import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from zipfile import ZipFile

app = FastAPI()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.post("/upload/")
async def upload(files: list[UploadFile] = File(...)):
    filenames = []
    for file in files:
        if allowed_file(file.filename):
            with open(file.filename, "wb") as f:
                shutil.copyfileobj(file.file, f)
            filenames.append(file.filename)

    zip_filename = 'archive.zip'
    with ZipFile(zip_filename, 'w') as zip:
        for filename in filenames:
            zip.write(filename)

    for filename in filenames:
        os.remove(filename)

    return FileResponse(zip_filename, headers={"Content-Disposition": f"attachment; filename={zip_filename}"})
