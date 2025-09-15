# ProdVision Django Project  

## 📋 Introduction  
**ProdVision** is a **PCB defect detection system** built with **Django** and **Computer Vision models (Faster R-CNN)**.  
The system supports **training, evaluation, and real-time defect detection** via a Django **REST API** and web-based UI.  

![image.png](/image.png)  

---

## 🚀 Features  
- Upload PCB images for **real-time defect detection**.  
- **REST API** for integration with external systems.  
- Model training and evaluation pipeline with **custom datasets**.  
- **Docker support** for easy deployment.  
- Frontend built with **Shadcn UI** for responsive design.  

---

## 🤖 Model  

### Dataset  
- Example training with: [Tiny-Defect-Detection-for-PCB](https://github.com/Ixiaohuihuihui/Tiny-Defect-Detection-for-PCB)  
- Supports **YOLO-format datasets**.  

### Architecture  
- **Faster R-CNN** for object detection.   
- Pipeline: `Input → Feature Extraction → RPN → Detection Head`.  

### Training Info  
- **Loss functions**: GIoU, Focal Loss.  
- **Optimizers**: SGD, Adam, AdamW.  
- **Hardware**: Trained on NVIDIA RTX 3050 (4GB).  
- Achieved **85% mAP** after optimization.  

### Advantages  
- High accuracy on small PCB defects.  
- Handles multiple object sizes.  

### Limitations  
- Requires GPU for efficient training.  
- Decreased accuracy on heavily occluded defects.  

---

## 🛠 Tech Stack  
- **Backend**: Python, Django, REST Framework  
- **Computer Vision**: PyTorch, Faster R-CNN, YOLOv8  
- **Frontend**: Shadcn UI, HTML/CSS, JavaScript  
- **Database**: PostgreSQL (via `.env` config)  
- **Deployment**: Docker, Docker Compose  

---

## 📂 Project Structure  
```bash
ProdVision_Django/
├── provision/ai_model   # Training scripts (Faster R-CNN, YOLOv8)
├── webapp/              # Django backend (API, views, serializers)
├── frontend/            # Shadcn UI frontend
├── dataset/             # PCB dataset (YOLO format)
├── docker-compose.yml
└── README.md
```  

---

## ⚙️ Getting Started  

### 1. Clone repositories  
```bash
# UI client
git clone https://github.com/vantoan2905/ProdVision_Ui.git
cd ProdVision_Ui

# Django server
git clone https://github.com/vantoan2905/ProdVision_django.git
cd ProdVision_django
```  

### 2. Train model  
```bash
cd provision/ai_model
python main.py --numclass 2 --mode train --model faster_rcnn --dataset coco --device cuda
```  

### 3. Setup `.env` file  
```env
POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DATABASE_URL=postgres://your_user:your_password@localhost:5432/your_db
SECRET_KEY=your_secret_key
```  

### 4. Install dependencies & run migrations  
```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```  

### 5. Run the server  
```bash
python manage.py runserver
```

### 6. Run with Docker  
```bash
docker-compose up --build
# Stop
docker-compose down
```  

---

## 📊 Results  
- **Training curve**:  
  ![Training Loss Curve](content/run/run1/loss_curve.png)  
- **Detection performance**: 85% mAP.  
- Logs & metrics in `results.csv`.  

---

## 📸 Demo  
- Updating!  

---

## 📌 Future Improvements  
- Add **MySQL/MongoDB integration** for storing detection history.  
- Enhance **real-time video streaming** with WebRTC.  
- Cloud deployment with **Docker + AWS/GCP**.  

---

## 📄 License  
MIT License  
