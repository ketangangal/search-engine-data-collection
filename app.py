from fastapi import FastAPI, File, UploadFile, Query
from src.components.database_helper import MysqlConnection
from src.components.s3_helper import S3Connection
from typing import List
import uvicorn

app = FastAPI(title="DataCollection-Server")

mysql = MysqlConnection()
mysql.create_connection()
mysql.setup_database()

sql = "select Label from ImageSearch.datacollection;"
dropDown = [label[0] for label in mysql.fetchall(sql)]
choices = Query("country", enum=dropDown)

s3 = S3Connection()


@app.post("/add_label/{label_name}")
def add_label(label_name: str):
    sql = f"INSERT INTO ImageSearch.datacollection (ID ,Label) VALUES (NULL ,'{label_name}');"
    response = mysql.insert(sql)
    if response[0]:
        response = s3.add_label(label_name)
        return {"Status": "Success", "S3-Response": response}
    else:
        return {"Status": "Fail", "Message": response[1]}


@app.post("/single_upload/")
async def single_upload(label: str = choices, file: UploadFile = None):
    if file.content_type == "image/jpeg":
        response = s3.single_upload(file.file, label)
        return {"filename": file.filename, "label": label, "S3-Response": response}
    else:
        return {"ContentType": f"Content type should be Image/jpeg not {file.content_type}"}


@app.post("/bulk_upload")
def bulk_upload(label: str = choices, files: List[UploadFile] = File(...)):
    try:
        skipped = []
        final_response = None
        for file in files:
            if file.content_type == "image/jpeg":
                response = s3.single_upload(file.file, label)
                final_response = response
            else:
                skipped.append(file.filename)
        return {"label": label, 'skipped': skipped, "S3-Response": final_response}
    except Exception as e:
        return {"ContentType": f"Content type should be Image/jpeg not {e}"}


if __name__ == "__main__":
    uvicorn.run("app:app", host='127.0.0.1', port=8080, reload=True)
