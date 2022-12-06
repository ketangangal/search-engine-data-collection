from src.utils.database_handler import MongodbClient
from src.utils.s3_handler import S3Connection
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Union, Any
import uvicorn


app = FastAPI(title="DataCollection-Server")
mongo = MongodbClient()
s3 = S3Connection()

choices = {}


# Fetch All Labels
@app.get("/fetch")
def fetch_label():
    try:
        global choices
        result = mongo.database['labels'].find()
        documents = [document for document in result]
        choices = dict(documents[0])
        response = {"Status": "Success", "Response": str(documents[0])}
        return JSONResponse(content=response, status_code=200, media_type="application/json")
    except Exception as e:
        raise e


# Label Post Api
@app.post("/add_label/{label_name}")
def add_label(label_name: str):
    result = mongo.database['labels'].find()
    documents = [document for document in result]
    last_value = list(map(int, list(documents[0].keys())[1:]))[-1]
    response = mongo.database['labels'].update_one({"_id": documents[0]["_id"]},
                                                   {"$set": {str(last_value + 1): label_name}})
    if response.modified_count == 1:
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
    label = choices.get(label, False)
    if file.content_type == "image/jpeg" and label != False:
        response = s3.upload_to_s3(file.file, label)
        return {"filename": file.filename, "label": label, "S3-Response": response}
    else:
        return {
            "ContentType": f"Content type should be Image/jpeg not {file.content_type}",
            "LabelFound": label,
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
        label: Union[bool, Any] = choices.get(label, False)
        if label:
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
                "LabelFound": label,
            }
        else:
            return {
                "label": label,
                "skipped": skipped,
                "S3-Response": final_response,
                "LabelFound": label,
            }
    except Exception as e:
        return {"ContentType": f"Content type should be Image/jpeg not {e}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
