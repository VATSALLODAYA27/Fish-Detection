FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 libxcb1 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY req.txt .
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r req.txt
COPY . .
CMD ["python", "app.py"]
