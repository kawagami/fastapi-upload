# FastAPI Firebase Storage API

本專案使用 FastAPI 建構，提供以下功能：
1. 圖片上傳至 Firebase Storage。
2. 列出已上傳的圖片。
3. 刪除指定圖片。
4. 使用 OpenCC 將簡體中文轉為繁體中文。

## 功能

### 1. 圖片上傳
**端點**: `POST /upload-image`  
**描述**: 上傳圖片至 Firebase Storage，返回圖片名稱與公開 URL。  
**請求範例**:
```bash
curl -X POST "http://localhost:8000/upload-image" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"
```

### 2. 列出圖片
**端點**: `GET /list-images`  
**描述**: 列出已上傳至 Firebase Storage 的所有圖片。  
**回應範例**:
```json
{
  "files": [
    {
      "name": "fastapi-upload/unique-id.jpg",
      "url": "https://your-firebase-storage-url/unique-id.jpg"
    }
  ]
}
```

### 3. 刪除圖片
**端點**: `DELETE /delete-image`  
**描述**: 刪除指定名稱的圖片。  
**請求範例**:
```json
{
  "file_name": "fastapi-upload/unique-id.jpg"
}
```

### 4. 簡體轉繁體
**端點**: `POST /convert-text`  
**描述**: 將簡體中文文本轉換為繁體中文。  
**請求範例**:
```json
{
  "text": "你好，世界"
}
```

**回應範例**:
```json
{
  "original_text": "你好，世界",
  "converted_text": "你好，世界"
}
```

---

## 安裝與運行

### 1. 安裝依賴
確保您已安裝 Docker，並執行以下指令以啟動專案：
```bash
docker build -t fastapi-firebase .
docker run -p 8000:8000 fastapi-firebase
```

### 2. 檔案結構
```
app/
├── main.py           # FastAPI 主程式
├── my-credentials.json # Firebase Admin SDK 憑證檔案
requirements.txt       # Python 依賴清單
Dockerfile             # Docker 配置檔案
```

### 3. Firebase 配置
請確保您的 Firebase 項目已設定 Storage，並將 Firebase Admin SDK 憑證檔案命名為 `my-credentials.json`，並放置於 `app/` 目錄下。

---

## 環境需求
- Python 3.9+
- Firebase Storage
- Docker

---

## 技術堆疊
- **FastAPI**: Web 框架
- **Firebase Admin SDK**: 處理 Firebase Storage
- **OpenCC**: 簡體/繁體中文轉換
