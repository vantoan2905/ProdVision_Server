
---

# Introduction  

# ProdVision Django Project  

**ProdVision** is a **defect detection system** built with **Django** and **Computer Vision models** such as **Faster R-CNN, YOLOv8**, and **UNet (for medical image analysis)**.  
It provides a complete pipeline for **training, evaluation, and real-time defect detection** via a **Django REST API** and a **web-based UI**.  
---
![alt text](main.png)




---

## Features  
- Upload PCB images for **real-time defect detection**.  
- **REST API** for integration with external systems.  
- Model training and evaluation pipeline with **custom datasets**.  
- **Docker support** for easy deployment.  
- Frontend built with **Shadcn UI** for responsive design.  

---

## Model  

### Dataset  
- Example dataset: [Tiny-Defect-Detection-for-PCB](https://github.com/Ixiaohuihuihui/Tiny-Defect-Detection-for-PCB)  
- Supports **YOLO-format datasets**.  

### Architecture  
- **Faster R-CNN** as main detection model.  
- Pipeline: `Input → Feature Extraction → RPN → Detection Head`.  

### Training Info  
- **Loss functions**: GIoU, Focal Loss  
- **Optimizers**: SGD, Adam, AdamW  
- **Hardware**: NVIDIA RTX 3050 (4GB)  README.rstREADME.rst
- Achieved **85% mAP** after optimization.  

### Advantages  
- High accuracy on small PCB defects.  
- Handles multiple object sizes.  

### Limitations  
- Requires GPU for efficient training.  
- Decreased accuracy on heavily occluded defects.  

---

## Tech Stack  
- **Backend**: Python, Django, Django REST Framework  
- **Computer Vision**: PyTorch, Faster R-CNN, YOLOv8, UNet  
- **Frontend**: Shadcn UI, HTML/CSS, JavaScript  
- **Database**: PostgreSQL (via `.env` config)  
- **Deployment**: Docker, Docker Compose  

---

## Project Structure  
```bash
ProdVision_Django/
├── app_django/          # Django project settings & configs
├── provision/           # Core app (AI models, services, APIs)
│   ├── ai_models/       # Training scripts (Faster R-CNN, YOLOv8, UNet)
│   ├── management/      # Custom management commands
│   ├── models/          # Database models
│   ├── serializers/     # DRF serializers
│   └── views/           # API views
├── media/               # Uploaded files (images, videos)
├── static/              # Static assets
├── docker-compose.yml
├── requirements.txt
└── README.md
````

---

## Getting Started

### 1. Clone repositories

```bash
# UI client
git clone https://github.com/vantoan2905/ProdVision_Ui.git
cd ProdVision_Ui

# Django server
git clone https://github.com/vantoan2905/ProdVision_Server.git
cd ProdVision_Server
```

### 2. Setup environment

Create `.env` file:

```env
POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DATABASE_URL=postgres://your_user:your_password@localhost:5432/your_db
SECRET_KEY=your_secret_key
```

### 3. Install dependencies & run migrations

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```



### 4. PostgreSQL Installation

See [PostgreSQL Setup Guide](docs/POSTGRESQL_SETUP.md).

After installation, create database:

```bash
python manage.py create_db
```

### 5. Run the server

```bash
python manage.py runserver
```
- Show Swagger view:
```bash
http://localhost:8000/docs
```
### 6. Run with Docker

```bash
docker compose up --build
# Stop
docker compose down
```

### 7. Model Training

See [Model Training Guide](provision/ai_models/README.md).

### 8. Pretrained Models

* [Download Faster R-CNN pretrained model](link_here)
* [Download YOLOv8 pretrained model](link_here)

---

## Notes

* Ensure you have **GPU + NVIDIA Container Toolkit** installed if you want GPU acceleration inside Docker.
* Logs, checkpoints, and results are stored in `checkpoints/` and `media/`.

```
