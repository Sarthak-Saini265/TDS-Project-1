"""
Test script to send a request to the API endpoint
"""
import requests
import json

# Read the test request
with open('test_request.json', 'r') as f:
    payload = json.load(f)

print("Sending test request to http://localhost:5000/api-endpoint")
print(f"Task: {payload['task']}")
print(f"Brief: {payload['brief'][:80]}...")
print("\nWaiting for response (this may take 1-2 minutes)...\n")

try:
    response = requests.post(
        'http://localhost:5000/api-endpoint',
        json=payload,
        headers={'Content-Type': 'application/json'},
        timeout=300  # 5 minutes timeout
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    
except requests.exceptions.Timeout:
    print("Request timed out (took longer than 5 minutes)")
except requests.exceptions.ConnectionError:
    print("Could not connect to server. Is it running?")
except Exception as e:
    print(f"Error: {e}")
