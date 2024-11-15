import json
import boto3
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# AWS S3 configuration
bucket_name = 'apimodelgrp-bkt'
object_key = 'models/pytorch-training-2024-11-15-05-36-37-084/profiler-output/system/incremental/2024111505/1731649020.algo-1.json'  

# Create a session using your AWS credentials
s3 = boto3.client('s3', region_name='us-east-2')

# response = s3.list_objects_v2(Bucket=bucket_name)
# if 'Contents' in response:
#     for obj in response['Contents']:
#         print(obj['Key'])
# else:
#     print("No objects found in the bucket.")

# Fetch the file from S3
response = s3.get_object(Bucket=bucket_name, Key=object_key)

file_content = response['Body'].read().decode('utf-8')

# Load the JSON data
data = [json.loads(line) for line in StringIO(file_content)]


# Convert to DataFrame
df = pd.DataFrame(data)

# Convert Timestamp to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

# Group by Type
grouped = df.groupby('Type')


# Plot time series for each type
plt.figure(figsize=(14, 8))

for name, group in grouped:
    plt.plot(group['Timestamp'], group['Value'], label=name)

plt.title('Time Series Graph by Type')
plt.xlabel('Timestamp')
plt.ylabel('Value')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()