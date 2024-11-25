from sagemaker.pytorch import PyTorchModel
import sagemaker

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()

# Define the model artifact location
model_artifact = "s3://apimodelgrp-bkt/models/pytorch-training-2024-11-15-13-17-06-795/output/model.tar.gz"

# Define the role with necessary permissions
role = sagemaker.get_execution_role()

# Create a SageMaker model object
pytorch_model = PyTorchModel(
    model_data=model_artifact,  # Path to model artifact in S3
    role=role,  # IAM role for SageMaker
    entry_point="inference.py",  # Your script for inference
    framework_version="2.0",  # Framework version matching your training
    py_version="py310",  # Python version
    sagemaker_session=sagemaker_session,
    source_dir="./source_dir"  # contains requirement.txt to install the requirements on the endpoint instance
)

predictor = pytorch_model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    # endpoint_name="apimodel-endpoint-2x"  # Optional, specify your own name, once it was created duplicate error will come if not changed
)


# If you don't specify endpoint_name, SageMaker generates a name like pytorch-inference-2024-11-15-12-34-56-789

endpoint_name = predictor.endpoint_name
print(f"Endpoint Name: {endpoint_name}")


# {
#     "input_text": "How to add a user?"
# } 