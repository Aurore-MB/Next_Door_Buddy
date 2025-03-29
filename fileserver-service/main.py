from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from minio import Minio
import io
import logging

import uvicorn

from uuid import uuid4


logger = logging.getLogger("uvicorn.error")


app = FastAPI()


minio_client = Minio(
    "minio-server:9000",
    access_key="GJq5sZzTSHExYDWnfqbZ",
    secret_key="1a76A8q47PQjS0buU7W2Mfsplz33lint10FfSQA2",
    secure=False
)


bucket_name = "test"


found = minio_client.bucket_exists(bucket_name)


if not found:
    minio_client.make_bucket(bucket_name)
    logger.info(f"Bucket '{bucket_name}'created un MinIO")
else:
    logger.info(f"Bucket '{bucket_name}' already ready on MinIO")


@app.get("/message")
async def home():
    return "Hello from the API !"

@app.post("/upload")
async def upload_file(my_file: UploadFile = File(...)):

    content = await my_file.read()

    size = len(content)

    extension = my_file.filename.split('.')[-1]

    storage_filename = f"{str(uuid4())}.{extension}"

    minio_client.put_object(
        bucket_name,
        storage_filename,
        io.BytesIO(content),
        length=size
    )

    return {
        "file": my_file.filename,
        "size": size,
        "message": "File successfully saved on MinIO !"
    }


@app.get("/download/{filename}")
async def download_file(filename: str):
    
    try:

        response = minio_client.get_object(bucket_name, filename)
        content_file = io.BytesIO(response.read())
        response.close()
        response.release_conn()

        return StreamingResponse(
            content_file,
            media_type="application/octet-stream",
            headers={
                'Content-Disposition': f"attachment; filename={filename}"
            }
        )

    except Exception as e:
        
        return {
            "error": "File is not found ou there's a problemn with MinIO",
            "details": str(e)
        }
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7004)
