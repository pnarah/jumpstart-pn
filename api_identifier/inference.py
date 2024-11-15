import torch
from torchvision import models
import os

# Define model loading function
def model_fn(model_dir):
    # Load the model from the specified directory
    model = models.resnet18(pretrained=False)
    model_path = os.path.join(model_dir, 'model.pth')
    model.load_state_dict(torch.load(model_path))
    return model

# Define input transformation function
def input_fn(request_body, request_content_type):
    # Transform the input data format into a PyTorch tensor
    # Here, we assume the input is JSON formatted
    if request_content_type == 'application/json':
        data = json.loads(request_body)
        tensor = torch.tensor(data)
        return tensor
    else:
        raise ValueError(f"Unsupported content type: {request_content_type}")

# Define prediction function
def predict_fn(input_data, model):
    # Make predictions using the model
    model.eval()
    with torch.no_grad():
        predictions = model(input_data)
    return predictions

# Define output transformation function
def output_fn(prediction, response_content_type):
    # Convert the prediction output to JSON
    if response_content_type == 'application/json':
        return json.dumps(prediction.tolist())
    else:
        raise ValueError(f"Unsupported content type: {response_content_type}")