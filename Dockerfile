FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg chromium libglib2.0-0 libnss3 libatk-bridge2.0-0 libx11-xcb1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
ENV SCRIPTORIA_ALLOWED_PATHS=/app/docs
CMD ["streamlit","run","app.py","--server.address=0.0.0.0","--server.port=8501"]
