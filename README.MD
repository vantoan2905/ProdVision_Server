# ProdVision Django Project  

## 📋 Introduction  

**ProdVision** is a PCB defect detection system built with **Django** and **YOLOv8**.  
The system supports model **training, evaluation**, and provides an **API** for PCB image defect detection.  

![image.png](/image.png)  

---

## 🤖 Model  

### 1. Dataset  
- Example training with custom data from:  
  [Tiny-Defect-Detection-for-PCB](https://github.com/Ixiaohuihuihui/Tiny-Defect-Detection-for-PCB)  

### 2. Training Result (10 epochs)  
![Training Loss Curve](content/run/run1/loss_curve.png)  

### 3. Model Name and Type  
- **Faster R-CNN + U-Net**  
- Combines object detection (Faster R-CNN) with segmentation (U-Net).  

### 4. Architecture Overview  
- **Backbone**: extracts image features.  
- **Region Proposal Network (RPN)**: generates candidate object regions.  
- **Detection Head**: classification + bounding box regression.  
- **U-Net**: segmentation for fine-grained detection.  

### 5. Working Mechanism  
`Input Image/Video → Feature Extraction → Region Proposals → Detection Head → Segmentation (U-Net)`  

Bounding boxes are predicted using **anchor-based** approach.  

### 6. Advantages  
- High accuracy (AP, mAP, F1-score).  
- Handles multiple objects, different sizes.  
- Supports segmentation for small PCB defects.  

### 7. Limitations  
- Requires significant computational resources (GPU/CPU).  
- Decreased accuracy for very small or heavily occluded defects.  

### 8. Reason for Selection  
- Well-suited for PCB dataset (many small objects).  
- Balances **accuracy** and **scalability**.  

### 9. Training Information  
- **Dataset**: YOLO-format PCB dataset.  
- **Loss functions**: GIoU Loss, Focal Loss.  
- **Optimizers**: SGD, Adam, AdamW.  
- **Hyperparameters**: batch size, learning rate.  

### 9. Dowload model pretrainz`:
- **Model**: 


---




## 🚀 Getting Started

### 1. Clone sever project and client Ui:
- Client (UI)::
```bash
git clone https://github.com/vantoan2905/ProdVision_Ui.git
cd ProdVision_Ui

```
- Sever project:
```bash
git clone https://github.com/your-username/ProdVision_django.git
cd ProdVision_django
```

- Open WSL2 (Ubuntu) and install NVIDIA Container Toolkit:
```bash
sudo apt-get update
sudo apt-get install -y curl gnupg2 ca-certificates lsb-release

```
- Add  key and repo:
```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

```
- Istall tollkit:
```bash
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```
- Docker runtime:
```bash
sudo nvidia-ctk runtime configure --runtime=docker
```
- Check GPU in Container:
```bash
docker run --rm --gpus all nvidia/cuda:12.6.2-base-ubuntu22.04 nvidia-smi
```


```bash
docker compose build

docker compose up -d
```


- Build docker image and run:

```bash
docker build -t prodvision_django . --no-cache
docker run --rm -it --gpus all -p 8000:8000 prodvision_django


```







<!-- -  Install NVIDIA Container Toolkit:
```bash
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```
- Check NVIDIA Container Toolkit:
```bash
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
``` -->




### 2. Training model
```bash
cd ProdVision_django/provision/ai_model
python main.py --numclass 2 --mode train --model faster_rcnn --dataset coco --device cuda


```

### 3. Set up the `.env` file:
```env
POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DATABASE_URL=postgres://your_user:your_password@localhost:5432/your_db
SECRET_KEY=your_secret_key
```

### 4. Install dependencies and run migrations:
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the server locally:
```bash
python manage.py runserver
uvicorn app_django.asgi:application --reload

```

### 6. Run with Docker:
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

