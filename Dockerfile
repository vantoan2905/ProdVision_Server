FROM nvidia/cuda:12.6.2-cudnn-runtime-ubuntu22.04

# Set env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ProdVision_django

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

COPY . .

RUN python3 manage.py collectstatic --noinput || true

CMD ["uvicorn", "app_django.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

