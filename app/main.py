from fastapi import FastAPI, File, UploadFile
import firebase_admin
from firebase_admin import credentials, storage
from uuid import uuid4

# 初始化 Firebase Admin SDK
cred = credentials.Certificate("/app/firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'fir-test-a67eb.appspot.com'
})

app = FastAPI()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # 讀取上傳的圖片檔案
        image_data = await file.read()

        # 生成唯一的檔案名稱
        file_name = f"fastapi-upload/{uuid4()}.jpg"

        # 將檔案上傳到 Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(file_name)
        blob.upload_from_string(image_data, content_type=file.content_type)

        # 取得圖片的公開 URL
        blob.make_public()
        image_url = blob.public_url

        return {"image_url": image_url}

    except Exception as e:
        return {"error": str(e)}