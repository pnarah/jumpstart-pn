import requests
import json
import boto3
import re

# endpoint_name = 'pytorch-inference-2024-11-25-08-41-17-750'
endpoint_name = 'pytorch-inference-2024-11-25-12-39-16-742'
runtime = boto3.client('sagemaker-runtime')

def parse_generated_text(text):
    # Regular expressions to extract relevant parts
    endpoint_pattern = r"endpoint:\s*(\S+)"
    method_pattern = r"method:\s*(\w+)"
    headers_pattern = r"headers:\s*(.*?)(?:data:|$)"
    email_pattern = r"'email':\s*'([^']*)'"
    team_id_pattern = r"'teamId':\s*(\d+)"
    param_pattern = r"params:\s*(.*?)(?:headers|data|$)"

    # Extract values using regular expressions, with fallback defaults
    endpoint = re.search(endpoint_pattern, text).group(1)
    method = re.search(method_pattern, text).group(1)

    headers_match = re.search(headers_pattern, text)
    headers_text = headers_match.group(1) if headers_match else ""
    params_match = re.search(param_pattern, text)
    params_text = params_match.group(1) if params_match else ""

    # Parse headers if present
    headers = {}
    if "'accept':" in headers_text:
        headers = {
            "accept": re.search(r"'accept':\s*'([^']+)'", headers_text).group(1),
        }
    if "'Content-Type':" in headers_text:
        headers['Content-Type'] = re.search(r"'Content-Type':\s*'([^']+)'", headers_text).group(1)

    # Extract specific data fields if present
    email_match = re.search(email_pattern, text)
    email = email_match.group(1) if email_match else None
    team_id_match = re.search(team_id_pattern, text)
    team_id = int(team_id_match.group(1)) if team_id_match else None

    # Parse params if present
    params = {}
    if "'dc_id':" in params_text:
        params["dc_id"] = re.search(r"'dc_id':\s*'(\d+)'", params_text).group(1)
    if "'team_id':" in params_text:
        params["team_id"] = re.search(r"'team_id':\s*'(\d+)'", params_text).group(1)

    # Construct the JSON structure based on extracted values
    formatted_output = {
        "endpoint": endpoint,
        "method": method,
        # "headers": headers,
        # "data": {}
    }

    # Add data or params based on extracted values
    if email and team_id is not None:
        formatted_output["data"] = {
            "email": email,
            "teamId": team_id
        }
    if "dc_id" in params or "team_id" in params:
        formatted_output["params"] = params  # For GET, we can treat it as params
    if headers:
        formatted_output["headers"] = headers

    return formatted_output


# Define the input data
# input_data ={
#     "inputs": "Get reservation for team 3"
# } 

while True: 
  message = input("User : ")
  if message:
    input_data ={
        "inputs": message
    } 
  # Invoke the endpoint
  response = runtime.invoke_endpoint(
      EndpointName=endpoint_name,
      ContentType='application/json',
      Body=json.dumps(input_data)
  )

  # Parse the response
  result = json.loads(response['Body'].read().decode())
  # print(result['result'])
  api_request = parse_generated_text(result['result'])
  print("Bot Response:", json.dumps(api_request, indent=2))
  # print("Parsed API Request:\n", json.dumps(api_request, indent=2))

  
  # test_input = "draw datum center from SPOG with datum center id six"
  # test_input="add user with e-mail id pnarah3@maildummy.com and team id 9"
#   generated_text = generate_api_request(test_input)
#   print("Generated Text:", generated_text)
#   api_request = parse_generated_text(generated_text)
#   print("Parsed API Request:\n", json.dumps(api_request, indent=2))