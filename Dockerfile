FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製所需的檔案
COPY requirements.txt .
COPY app/ /app/

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 FastAPI 使用的端口
EXPOSE 8000

# 啟動 FastAPI 應用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
