import requests
import json
import boto3

endpoint_name = 'apimodel-endpoint-1'
runtime = boto3.client('sagemaker-runtime')

# Define the input data
input_data = {
    "input_text": "Get reservation for team 3"
}

# Invoke the endpoint
response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='application/json',
    Body=json.dumps(input_data)
)

# Parse the response
result = json.loads(response['Body'].read().decode())
print(result)

  
  # test_input = "draw datum center from SPOG with datum center id six"
  # test_input="add user with e-mail id pnarah3@maildummy.com and team id 9"
#   generated_text = generate_api_request(test_input)
#   print("Generated Text:", generated_text)
#   api_request = parse_generated_text(generated_text)
#   print("Parsed API Request:\n", json.dumps(api_request, indent=2))