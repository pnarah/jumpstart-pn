from sagemaker.pytorch import PyTorch
import sagemaker

# Initialize SageMaker session and get the role
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

import os
print("Current working directory:", os.getcwd())

# Specify S3 paths
# bucket = 'apimodelgrp-bkt'
# training_data_path = f's3://{bucket}/trainingdata/'
# output_path = f's3://{bucket}/models/'

# Specify S3 paths
bucket = 'mystoragebucket-ohio'
training_data_path = f's3://{bucket}/trainingdata/'
output_path = f's3://{bucket}/spogapplicationmodel/'

# Define the PyTorch Estimator
estimator = PyTorch(
    entry_point='train.py',
    role=role,
    framework_version='2.0',
    py_version='py310',
    instance_count=1,
    instance_type='ml.m5.xlarge',
    output_path=output_path,
    sagemaker_session=sagemaker_session,
    dependencies=['./requirements.txt', './inference.py'],
)

# Start the training job with the specified training data
estimator.fit({'training': training_data_path})


# Deploy the model
predictor = estimator.deploy(
    initial_instance_count=1,
    instance_type='ml.m5.xlarge',
    entry_point='inference.py',
    # endpoint_name="spogmodel-endpoint-01"
)
