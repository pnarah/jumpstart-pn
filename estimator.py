from sagemaker.pytorch import PyTorch
import sagemaker

# Initialize SageMaker session and get the role
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

import os
print("Current working directory:", os.getcwd())

# Specify S3 paths
bucket = 'apimodelgrp-bkt'
training_data_path = f's3://{bucket}/trainingdata/'  # Path to training data in S3
output_path = f's3://{bucket}/models/'  # Where to save model artifacts in S3

# Define the PyTorch Estimator
estimator = PyTorch(
    entry_point='train.py',             # Path to your training script
    role=role,
    framework_version='1.10',            # Ensure compatibility with your dependencies
    py_version='py38',
    instance_count=1,
    instance_type='ml.m5.2xlarge',      # Instance type for training
    output_path=output_path,            # S3 location to save model artifacts
    sagemaker_session=sagemaker_session,
    dependencies=['./requirements.txt']
)

# Start the training job with the specified training data
estimator.fit({'training': training_data_path})