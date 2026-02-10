FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY . .

# 设置环境变量默认值
ENV PORT=8000
ENV API_KEY=admin123
ENV CORS_ORIGINS="*"

# 启动命令
CMD uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT
