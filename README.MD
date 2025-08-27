# Introduction project:
# ProdVision Django Project
## 📋 Project Introduction

ProdVision is a PCB defect detection system using YOLOv8, built with Django. The project supports model training, evaluation, and provides an API for PCB image defect detection.

![image.png](/image.png)

# Model

## 1. Model Name and Type
- **Faster R-CNN + U-Net**  
- A combination of object detection (Faster R-CNN)   

## 2. Architecture Overview
- **Backbone**: extracts features from the input image.  
- **Region Proposal Network (RPN)**: generates candidate regions that may contain objects.  
- **Detection Head**: performs classification and bounding box regression.  
- **U-Net**: provides detailed segmentation, enhancing detection quality.  

## 3. Working Mechanism
- Pipeline: `Input video from camera → Feature Extraction → Region Proposals → Classification + Regression → Segmentation (U-Net)`  
- Bounding boxes are predicted using an **anchor-based** approach.  

## 4. Advantages
- High accuracy (AP, mAP, F1-score).  
- Capable of handling multiple objects and different object sizes.  
- Supports fine-grained segmentation through U-Net.  

## 5. Limitations
- Requires significant computational resources (GPU/CPU).  
- Accuracy decreases for very small or heavily occluded objects.  

## 6. Reason for Selection
- Well-suited for the dataset in this project (many small objects, real-time environment, limited hardware).  
- Compared to other models, Faster R-CNN + U-Net provides a strong balance between **accuracy** and **scalability**.  

## 7. Training Information
- **Dataset**: used for training/finetuning.  
- **Loss functions**: GIoU Loss, Focal Loss,…  
- **Optimizers**: SGD, Adam, AdamW.  
- **Hyperparameters**: batch size, learning rate,…  






## 🚀 Getting Started

### 1. Clone sever project and client Ui:
- Client project:
```bash
git clone https://github.com/vantoan2905/ProdVision_Ui.git
cd ProdVision_Ui

```
- Sever project:
```bash
git clone https://github.com/your-username/ProdVision_django.git
cd ProdVision_django
```

### 2. Set up the `.env` file:
```env
POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DATABASE_URL=postgres://your_user:your_password@localhost:5432/your_db
SECRET_KEY=your_secret_key
```

### 3. Install dependencies and run migrations:
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run the server locally:
```bash
python manage.py runserver
uvicorn app_django.asgi:application --reload

```

### 5. Run with Docker:
```bash
docker-compose up --build
# To stop:
docker-compose down
```

---

## 📝 Notes

- Training data follows YOLO format.
- Evaluation based on the validation set in `data.yaml`.
- Detailed epoch results in `results.csv`.

---

## 📄 License

This project is licensed under the MIT

