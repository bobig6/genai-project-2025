# Museum Quiz System

## 1. Introduction

- **Project Name:** Museum Quiz System  
- **Course:** Intelligent Agents with Generative AI – 2024 / 2025  
- **Author:** Boyan Ivanov (Faculty Number: 0MI0800011)  
- **GitHub Repository:** [Museum Quiz System](https://github.com/bobig6/genai-project-2025)  
- **Dataset:** [photos.zip](https://drive.google.com/file/d/1ZY_WbA-Fd4qw5YFBzw4P0LlLCNWVl5VE/view?usp=sharing)
- **Unity Project**: [generation_and_mobile_project.unitypackage](https://drive.google.com/file/d/1NyGZJlZZl8DqWJKnAy7f_KxRXeZk8rzK/view?usp=sharing)  
- **Inspired by**: [Faster R-CNN on custom dataset Using Pytorch](https://www.youtube.com/watch?v=xYd95gppJ-0&ab_channel=CodeWithAarohi)

- **Short Description:**  
  - Identifies museum exhibits from user-submitted images.  
  - Uses Faster R-CNN for object detection.  
  - Developed with Unity, Python FastAPI, and PyTorch.  

---

## 2. Business Needs

- Provides an interactive educational experience for museum visitors.  
- Uses machine learning to detect museum artifacts.  

---

## 3. System Overview

### Client Application (Unity)
- Users capture images using the device camera.  
- Images are sent to the backend for validation.  

### Server (FastAPI)
- Handles API requests.  
- Manages object detection and model uploads.  

### ML Model (Faster R-CNN)
- Detects exhibits in images.  
- Supports training with synthetic and real data.  

---

## 4. Key Features

### User Role
- Capture and submit exhibit images.  
- Receive validation feedback.  

### Admin Role
- Upload and update ML models.  
- Manage exhibit datasets.  

### ML Model & Data
- Faster R-CNN with PyTorch.  
- Dataset Format: COCO JSON.  

### Synthetic Data Generation
- Uses Unity to generate synthetic images with background variation and random transformations.  
- Labeled in COCO JSON format.  

### 3D Object Scanning
- **Tool:** [PolyCam](https://poly.cam/) (Mobile app for 3D scanning).  
- Generates 3D models from multiple images.  

### Image Labeling
- **Tool:** [VGG Image Annotator (VIA)](https://www.robots.ox.ac.uk/~vgg/software/via/)  
- Labels exported in COCO JSON format.  

---

## 5. Agent System Description (PEAS)

| Agent                     | Performance Measure       | Environment              | Actuators               | Sensors                   |
|---------------------------|-------------------------|--------------------------|-------------------------|---------------------------|
| User Interaction Agent    | High user experience    | Unity Mobile App        | Sends images to server  | Captures images           |
| Prediction Server Agent   | Fast & accurate results | FastAPI Backend         | Returns prediction      | Receives images via API   |
| ML Model Trainer Agent   | High detection accuracy | Local training machine  | Saves/upload models    | Receives datasets        |
| Synthetic Data Generator  | High-quality data      | Local generation tool   | Generates images       | Uses 3D models           |
| 3D Scanning App          | Accurate 3D scanning   | Mobile application      | Generates 3D mesh      | Receives object images   |
| Image Labeling Agent     | Accurate data labeling | Web-based tool (VIA)   | Labels images          | Receives images          |

---

## 6. System Architecture

### Unity Mobile App
- **Main Scene:** Buttons for recognized objects.  
- **Camera Scene:** Users take pictures and send them for prediction.  
- **Results Scene:** Displays results with detected objects.  

### Server (FastAPI)
- **Endpoints:**
  - `/predict`: Sends an image and receives exhibit detection results.  
  - `/admin`: Uploads and manages ML models.  

### Training Process
- **Dependencies Setup:**
  ```sh
  py -3.10 -m venv myvenv
  myvenv\Scripts\activate
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
  python -m pip install --upgrade pip
  pip install pycocotools jupyter notebook
  ```
- **CUDA Installation:** Uses CUDA 12.1 for GPU acceleration.  
- **Run Training:**
  ```sh
  jupyter notebook
  ```
- **Training Notebook:** `train_FasterRCNN.ipynb`
  - Cell 9: Test single images.  
  - Cell 10: Test with camera input.  
  - Cell 11: Evaluate precision, recall, F1-score.  

---

## 7. Model Training Process

### Model Selection
- **Architecture:** Faster R-CNN with ResNet-50 backbone.  
- **Pre-trained Model:** COCO-trained Faster R-CNN with Feature Pyramid Networks (FPN).  
- **Modifications:**
  - Custom classification head for 7 classes (1 background + 6 objects).  

### Dataset Preparation
- **Annotation Format:** COCO JSON.  
- **Data Augmentation:** Minimal (tensor conversion).  
- **Splitting:** 80% training, 20% testing.  

### Training Configuration
- **Hardware:** GPU (CUDA 12.1) preferred.  
- **Batch Size:** 4  
- **Optimizer:** SGD (Momentum: 0.9, Learning Rate: 0.005)  
- **Scheduler:** StepLR (Step Size: 3, Gamma: 0.1)  
- **Epochs:** Infinite training, checkpoints every 5 epochs.  

### Evaluation Metrics
- **IoU Threshold:** 0.5  
- **Precision, Recall, F1-score Calculated**  

---

## 8. Training and Testing Data

| Object         | Images | Synthetic | Notes |
|---------------|--------|-----------|------------------------------------------------|
| Wallet        | 195    | No        | High front & back accuracy, poor side detection |
| Car           | 70     | No        | Good front & back, low side/top accuracy        |
| Dho Badge     | 60     | 59        | 3D printed, high accuracy                        |
| Battery Case  | 213    | 90        | Medium accuracy, sometimes misidentified        |
| Deer          | 144    | 53        | 3D scanned, moderate accuracy                   |
| Skull         | 33     | 138       | Highest accuracy, well-recognized from all angles |

---

## 9. Results & Conclusions

- **Trained for 128 epochs** (main improvements in first 5 epochs).  
- **Final Model Evaluation:**  
  - **Precision:** 0.9795  
  - **Recall:** 0.9845  
  - **F1 Score:** 0.982  

- **Findings:**  
  - Best results were achieved with **low natural images + high synthetic data**.  
  - 3D scanned models helped improve accuracy.  
  - Training on **new objects requires retraining**; incremental training needed.  

- **Future Improvements:**  
  - Streamline synthetic data generation.  
  - Automate dataset labeling.  
  - Implement incremental training to add new objects without full retraining.  

---

## 10. Repository Structure

```
📂 MuseumQuizSystem
├── 📂 unity/  
│   ├── generation_and_mobile_project.unitypackage  
├── 📂 training/  
│   ├── train_FasterRCNN.ipynb  
│   ├── requirements.txt  
├── 📂 server/  
│   ├── main.py (FastAPI server)  
│   ├── models/ (Pre-trained models)  
├── photos.zip
├── README.md  
```

---

## 11. How to Run the System

### 1. Clone the Repository
```sh
git clone https://github.com/bobig6/genai-project-2025
cd genai-project-2025
```

### 2. Install Dependencies
```sh
py -3.10 -m venv myvenv
myvenv\Scripts\activate
pip install -r training/requirements.txt
```

### 3. Start the Server
```sh
cd server
docker build -t boyanii/gen-ai-project:server-ver-1 .
docker run -p 80:80 boyanii/gen-ai-project:server-ver-1
```

### 4. Run Training (Optional)
```sh
jupyter notebook training/train_FasterRCNN.ipynb
```

### 5. Run Unity Mobile App
- Open `unity/generation_and_mobile_project.unitypackage` in Unity.
- Build and deploy the app.

---

## 12. License

MIT License. See `LICENSE` for details.
```

This `README.md` file provides a structured, detailed overview of the project, including installation instructions, system architecture, dataset structure, and evaluation results. 🚀