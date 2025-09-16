

---

# Model Training Guide

## 1. Prerequisites

* Python 3.9+
* [PostgreSQL](https://www.postgresql.org/download/) (if using database storage)
* Install dependencies:

```bash
pip install -r requirements.txt
```

## 2. Project Structure (Simplified)

```
provision/
│── ai_models/
│   ├── yolo/
│   ├── faster_R_CNN/
│   ├── mask_R_CNN/
│   ├── SSD/
│   └── Unet/
│── data_loader/
│── main.py
│── test.py
```

## 3. Prepare Dataset

* Put your dataset inside the `data/` folder.
* If folder `data/` does not exist run command:
```bash
mkdir data
```
* Expected format (example YOLO):

  ```
  data/
  ├── images/
  │   ├── train/
  │   └── val/
  └── labels/
      ├── train/
      └── val/
  ```

## 4. Train the Model

Run training with the desired model (example: YOLO):
* For YOLO:
```bash
cd provision/ai_model
python provision/ai_models/yolo/train.py --config configs/yolo.yaml
```
* For Faster RCNN:
```bash
cd provision/ai_model
python main.py --numclass 2 --mode train --model faster_rcnn --dataset coco --device cuda
```  


## 5. Evaluate the Model

```bash
python provision/ai_models/test.py --model-path checkpoints/best_model.pth
```

## 6. Inference

```bash
python provision/ai_models/main.py --input path/to/image.jpg --model yolo
```

## 7. Save & Export Model

* Trained weights will be stored in `checkpoints/`.
* You can export to ONNX/TorchScript using:

```bash
python provision/ai_models/export.py --model yolo --weights checkpoints/best_model.pth
```

---


---

## 📊 Results  
- **Training curve**:  
  
  D:\pcb_defect\ProdVision_django\content\run\run1\loss_curve.png 
  ![Training Loss Curve](../../content/run/run1/loss_curve.png)
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
