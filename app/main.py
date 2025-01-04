from fastapi import FastAPI, File, UploadFile, HTTPException
import firebase_admin
from firebase_admin import credentials, storage
from uuid import uuid4
from pydantic import BaseModel
from opencc import OpenCC

# 初始化 Firebase Admin SDK
cred = credentials.Certificate("/app/my-credentials.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'fir-test-a67eb.appspot.com'
})

app = FastAPI()

# 定義 MIME 類型和副檔名的對應
mime_type_extension = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif"
}

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # 讀取上傳的圖片檔案
        image_data = await file.read()

        # 根據 MIME 類型取得副檔名
        file_extension = mime_type_extension.get(file.content_type, ".png")
        
        # 生成唯一的檔案名稱，包含正確的副檔名
        file_name = f"fastapi-upload/{uuid4()}{file_extension}"

        # 將檔案上傳到 Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(file_name)
        blob.upload_from_string(image_data, content_type=file.content_type)

        # 取得圖片的公開 URL
        blob.make_public()
        image_url = blob.public_url

        # 返回與 /list-images 一致的結構
        return {
            "name": file_name,
            "url": image_url
        }

    except Exception as e:
        return {"error": str(e)}

@app.get("/list-images")
def list_images():
    try:
        # 列出所有檔案
        bucket = storage.bucket()
        blobs = bucket.list_blobs(prefix="fastapi-upload/")  # 僅列出特定前綴的檔案
        
        # 收集檔案名稱和公開 URL
        files = []
        for blob in blobs:
            files.append({
                "name": blob.name,
                "url": blob.public_url
            })

        return {"files": files}

    except Exception as e:
        return {"error": str(e)}

# 定義請求體的格式
class DeleteImageRequest(BaseModel):
    file_name: str  # 要刪除的檔案名稱

@app.delete("/delete-image")
def delete_image(request: DeleteImageRequest):
    try:
        # 取得檔案名稱
        file_name = request.file_name

        # 刪除指定檔案
        bucket = storage.bucket()
        blob = bucket.blob(file_name)

        if not blob.exists():
            raise HTTPException(status_code=404, detail="File not found")

        blob.delete()
        return {"message": f"File '{file_name}' deleted successfully"}

    except Exception as e:
        return {"error": str(e)}

# 定義簡體轉繁體的請求體結構
class ConvertTextRequest(BaseModel):
    text: str  # 要轉換的簡體中文文本

# 初始化 OpenCC
opencc = OpenCC("s2t.json")  # 簡體轉繁體

@app.post("/convert-text")
def convert_text(request: ConvertTextRequest):
    try:
        # 使用 OpenCC 進行文本轉換
        converted_text = opencc.convert(request.text)
        return {"original_text": request.text, "converted_text": converted_text}
    except Exception as e:
        return {"error": str(e)}
