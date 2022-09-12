from typing import List

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from src.components.database_handler import MysqlConnection
from src.components.queries import ADD_LABEL, FETCH_LABELS, database, table
from src.components.s3_handler import S3Connection

# Setup all the connection
app = FastAPI(title="DataCollection-Server")
mysql = MysqlConnection()
s3 = S3Connection()

choices = {}


# Fetch All Labels
@app.get("/fetch")
def fetch_label():
    global choices
    status, result = mysql.fetchall(FETCH_LABELS)
    if status:
        choices = {value[0]: True for key, value in enumerate(result)}
        return {"Status": "Success", "S3-Response": choices}
    else:
        return {"Status": "Failed", "S3-Response": result}


# Label Post Api
@app.post("/add_label/{label_name}")
def add_label(label_name: str):
    response = mysql.insert(ADD_LABEL.format(database, table, label_name))
    if response[0]:
        response = s3.add_label(label_name)
        return {"Status": "Success", "S3-Response": response}
    else:
        return {"Status": "Fail", "Message": response[1]}


@app.get("/single_upload/")
def single_upload():
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]}
    return JSONResponse(content=info, status_code=200, media_type="application/json")


# Image Single Upload Api
@app.post("/single_upload/")
async def single_upload(label: str, file: UploadFile = None):
    status = choices.get(label, False)
    if file.content_type == "image/jpeg" and status:
        response = s3.upload_to_s3(file.file, label)
        return {"filename": file.filename, "label": label, "S3-Response": response}
    else:
        return {
            "ContentType": f"Content type should be Image/jpeg not {file.content_type}",
            "LabelFound": status,
        }


@app.get("/bulk_upload")
def bulk_upload():
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]}
    return JSONResponse(content=info, status_code=200, media_type="application/json")


# Transforms here
@app.post("/bulk_upload")
def bulk_upload(label: str, files: List[UploadFile] = File(...)):
    try:
        skipped = []
        final_response = None
        status = choices.get(label, False)
        if status:
            for file in files:
                if file.content_type == "image/jpeg":
                    response = s3.upload_to_s3(file.file, label)
                    final_response = response
                else:
                    skipped.append(file.filename)
            return {
                "label": label,
                "skipped": skipped,
                "S3-Response": final_response,
                "LabelFound": status,
            }
        else:
            return {
                "label": label,
                "skipped": skipped,
                "S3-Response": final_response,
                "LabelFound": status,
            }
    except Exception as e:
        return {"ContentType": f"Content type should be Image/jpeg not {e}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
