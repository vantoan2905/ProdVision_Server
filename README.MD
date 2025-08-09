# Introduction project:
- 



- 

# Server runer:
* First clone project:
```bash

```


1. Run in local:
```bash
uvicorn main:app --reload
```
2. Run with docker:
```bash

```

# YOLOv8 Training Report 

## 1. Model performance:

1. Configuration file: args.yaml
   - Information: model, dataset, epochs, batch size, image size, device, augmentation.

## 2. 📉 Loss & mAP Charts:

- `results.png`: Hiển thị loss (box, obj, cls) và mAP50, mAP50-95  
<img src="src/process/content/runs/detect/train3/results.png" alt="results.png" width="800"/>

---

## 3. 🎯 Per-Class Accuracy:

- `BoxF1_curve.png`  
<img src="src/process/content/runs/detect/train3/BoxF1_curve.png" alt="F1 Curve" width="600"/>

- `BoxP_curve.png`  
<img src="src/process/content/runs/detect/train3/BoxP_curve.png" alt="Precision Curve" width="600"/>

- `BoxPR_curve.png`  
<img src="src/process/content/runs/detect/train3/BoxPR_curve.png" alt="PR Curve" width="600"/>

- `BoxR_curve.png`  
<img src="src/process/content/runs/detect/train3/BoxR_curve.png" alt="Recall Curve" width="600"/>

---

## 4. 📊 Confusion Matrix:

- `confusion_matrix_normalized.png`  
<img src="src/process/content/runs/detect/train3/confusion_matrix_normalized.png" alt="Confusion Matrix Normalized" width="600"/>

- `confusion_matrix.png`  
<img src="src/process/content/runs/detect/train3/confusion_matrix.png" alt="Confusion Matrix" width="600"/>
## 2. 📉 Loss & mAP Charts:

- `results.png`: Hiển thị loss (box, obj, cls) và mAP50, mAP50-95  
<img src="src/process/content/runs/detect/train3/results.png" alt="results.png" width="600"/>

---



5. Sample labels and predictions:
   - train_batch*.jpg: training images
   - val_batch*_labels.jpg: ground truth
   - val_batch*_pred.jpg: prediction

6. Weights:
   - weights/best.pt: best model
   - weights/last.pt: final model

------------------------------------------------------------

Model reuse suggestion:
    yolo task=detect mode=predict model=weights/best.pt source=path/to/images

Notes:
- Training data follows YOLO format
- Evaluation based on validation set in data.yaml
- Detailed epoch results in results.csv
