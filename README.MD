# Introduction project:
# ProdVision Django Project

## 📋 Project Introduction

ProdVision is a PCB defect detection system using YOLOv8, built with Django. The project supports model training, evaluation, and provides an API for PCB image defect detection.

![alt text](provision/media/main_view.png)

## 🚀 Getting Started

### 1. Clone the project:
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

## 🧠 YOLOv8 Training Report

### 1. Model Configuration

- Configuration file: `args.yaml`
- Includes: model, dataset, epochs, batch size, image size, device, augmentation.

### 2. 📉 Loss & mAP Charts

- `results.png`: Shows loss (box, obj, cls) and mAP50, mAP50-95  
<img src="src/process/content/runs/detect/train3/results.png" alt="results.png" width="800"/>

---

### 3. 🎯 Per-Class Accuracy

- `BoxF1_curve.png`  
<img src="src/process/content/runs/detect/train3/BoxF1_curve.png" alt="F1 Curve" width="600"/>

- `BoxP_curve.png`  
<img src="src/process/content/runs/detect/train3/BoxP_curve.png" alt="Precision Curve" width="600"/>

- `BoxPR_curve.png`  
<img src="src/process/content/runs/detect/train3/BoxPR_curve.png" alt="PR Curve" width="600"/>

- `BoxR_curve.png`  
<img src="src/process/content/runs/detect/train3/BoxR_curve.png" alt="Recall Curve" width="600"/>

---

### 4. 📊 Confusion Matrix

- `confusion_matrix_normalized.png`  
<img src="src/process/content/runs/detect/train3/confusion_matrix_normalized.png" alt="Confusion Matrix Normalized" width="600"/>

- `confusion_matrix.png`  
<img src="src/process/content/runs/detect/train3/confusion_matrix.png" alt="Confusion Matrix" width="600"/>

---

### 5. Sample Labels and Predictions

- `train_batch*.jpg`: Training images
- `val_batch*_labels.jpg`: Ground truth
- `val_batch*_pred.jpg`: Predictions

### 6. Model Weights

- `weights/best.pt`: Best model
- `weights/last.pt`: Final model

---

## 🔁 Model Reuse

```bash
yolo task=detect mode=predict model=weights/best.pt source=path/to/images
```

---

## 📝 Notes

- Training data follows YOLO format.
- Evaluation based on the validation set in `data.yaml`.
- Detailed epoch results in `results.csv`.

---

## 📄 License

This project is licensed under the MIT

