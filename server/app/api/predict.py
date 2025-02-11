from fastapi import APIRouter, File, UploadFile, Form
import io
import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.transforms import functional as F
from PIL import Image

router = APIRouter()

# Global variables to hold the current model and device.
model = None
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# -----------------------------------------------------------------------------
# Define the mapping from label indices to class names.
# Adjust these class names to match your training.
COCO_CLASSES = {
    1: "wallet",
    2: "car",
    3: "dho_badge",
    4: "battery_case",
    5: "deer",
    6: "skull",
    7: "background"  # Adjust if background is handled differently.
}

def get_class_name(class_id):
    return COCO_CLASSES.get(class_id, "Unknown")

# -----------------------------------------------------------------------------
# Define a helper function to get a Faster R-CNN model with a custom head.
def get_model(num_classes: int):
    # Load a pre-trained Faster R-CNN model with a ResNet-50 backbone and FPN.
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    # Get the number of input features for the classifier head.
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # Replace the pre-trained head with a new one for our custom number of classes.
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model

# -----------------------------------------------------------------------------
# Function to load the model weights from the specified model path.
def load_model(model_path: str):
    global model
    num_classes = 7  # Example: Background + 6 object classes. Adjust as needed.
    model = get_model(num_classes)
    # Load the trained weights (ensure that the file exists at model_path).
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()  # Set the model to evaluation mode.
    print("Model loaded successfully.")

# -----------------------------------------------------------------------------
# A helper function that performs prediction on a PIL image.
def predict_image(pil_image: Image.Image, threshold: float = 0.5):
    # Convert the PIL image to a tensor and add a batch dimension.
    image_tensor = F.to_tensor(pil_image).unsqueeze(0).to(device)

    # Perform inference without computing gradients.
    with torch.no_grad():
        prediction = model(image_tensor)

    predictions = []
    # Extract boxes, labels, and scores from the prediction.
    boxes = prediction[0]['boxes'].cpu().numpy()
    labels = prediction[0]['labels'].cpu().numpy()
    scores = prediction[0]['scores'].cpu().numpy()

    # Loop over each detection and filter out predictions below the threshold.
    for box, label, score in zip(boxes, labels, scores):
        if score > threshold:
            predictions.append({
                "box": box.astype(int).tolist(),
                "class": get_class_name(label),
                "score": float(score)
            })
    return predictions

# -----------------------------------------------------------------------------
# Define the prediction endpoint.
# This endpoint accepts an image file, the target class name, and a threshold.
@router.post("/predict")
async def predict_exhibit(
    file: UploadFile = File(...),
    target_class: str = Form(...),
    threshold: float = Form(0.5)
):
    global model
    # If the model has not been loaded yet, load it using the default model path.
    if model is None:
        load_model("training2_128_epoch/fasterrcnn_resnet50_epoch_55.pth")

    # Read the uploaded file.
    contents = await file.read()
    # Open the image using PIL and ensure it is in RGB mode.
    pil_image = Image.open(io.BytesIO(contents)).convert("RGB")

    # Run predictions on the image.
    preds = predict_image(pil_image, threshold=threshold)

    # Check if any prediction matches the target class (ignoring case).
    detected = any(pred["class"].lower() == target_class.lower() for pred in preds)

    # Return true if the target class was detected, false otherwise.
    return {"detected": detected, "predictions": preds}
