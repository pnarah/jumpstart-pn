import json
import os
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Create a custom dataset
class APIDataset(Dataset):
    def __init__(self, input_encodings, target_encodings):
        self.input_encodings = input_encodings
        self.target_encodings = target_encodings

    def __len__(self):
        return len(self.input_encodings.input_ids)

    def __getitem__(self, idx):
        return {
            "input_ids": self.input_encodings.input_ids[idx],
            "attention_mask": self.input_encodings.attention_mask[idx],
            "labels": self.target_encodings.input_ids[idx]
        }

def train():
    # Initialize tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    model = T5ForConditionalGeneration.from_pretrained("t5-base")

    # Load the training data from the SageMaker directory
    training_data_path = os.path.join('/opt/ml/input/data/training', 'augmented_training_data_10var.json')
    with open(training_data_path, 'r') as f:
        training_data = json.load(f)

    # Prepare training data
    input_texts = [data["input_text"] for data in training_data]
    target_texts = []
    for data in training_data:
        api_request = data.get("api_request", {})
        params_str = str(api_request.get("params", {}))
        headers_str = str(api_request.get("headers", {}))
        data_str = str(api_request.get("data", {}))
        target_texts.append(
            f'endpoint: {api_request.get("endpoint", "")} method: {api_request.get("method", "")} params: {params_str} headers: {headers_str} data: {data_str}'
        )

    # Tokenize the input and target text
    input_encodings = tokenizer(input_texts, padding=True, truncation=True, return_tensors="pt")
    target_encodings = tokenizer(target_texts, padding=True, truncation=True, return_tensors="pt")

    # Instantiate dataset and dataloader
    dataset = APIDataset(input_encodings, target_encodings)
    loader = DataLoader(dataset, batch_size=2, shuffle=True)

    # Define training loop
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    model.train()

    for epoch in range(3):
        epoch_loss = 0
        correct_predictions = 0
        total_predictions = 0
        for batch in loader:
            optimizer.zero_grad()
            outputs = model(input_ids=batch["input_ids"],
                            attention_mask=batch["attention_mask"],
                            labels=batch["labels"])
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            predictions = torch.argmax(outputs.logits, dim=-1)
            correct_predictions += (predictions == batch["labels"]).sum().item()
            total_predictions += batch["labels"].numel()

        avg_epoch_loss = epoch_loss / len(loader)
        epoch_accuracy = correct_predictions / total_predictions
        print(f"Epoch {epoch + 1}, Average Loss: {avg_epoch_loss}, Accuracy: {epoch_accuracy}")

    # Save the trained model to the specified directory
    model_dir = os.environ.get('SM_MODEL_DIR', '/opt/ml/model')
    model_save_path = os.path.join(model_dir, 'apimodel.pth')
    torch.save(model.state_dict(), model_save_path)

if __name__ == '__main__':
    train()
