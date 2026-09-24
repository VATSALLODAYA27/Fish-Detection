FROM python:3.11-slim
WORKDIR /app
COPY req.txt .
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r req.txt
COPY . .
CMD ["python", "app.py"]
