# 基於 Python 3.13-alpine 映像
FROM python:3.13-alpine

# 安裝編譯工具和 OpenCC 相關依賴
RUN apk add --no-cache \
    build-base \
    cmake \
    gcc \
    g++ \
    musl-dev \
    linux-headers

# 設定工作目錄
WORKDIR /app

# 複製所需的檔案
COPY requirements.txt .
COPY app/ /app/

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 清理編譯工具（可選，節省空間）
RUN apk del build-base cmake gcc g++ musl-dev linux-headers

# 暴露 FastAPI 使用的端口
EXPOSE 8000

# 啟動 FastAPI 應用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
