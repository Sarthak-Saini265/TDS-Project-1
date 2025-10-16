"""
Send a test request with a unique task name
"""
import requests
import json
from datetime import datetime
import random

# Generate a unique task name
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
random_id = random.randint(1000, 9999)
task_name = f"test-app-{timestamp}-{random_id}"

# Create the payload
payload = {
    "email": "student@example.com",
    "secret": "geralt_of_rivia",
    "task": task_name,
    "round": 1,
    "nonce": f"test-nonce-{random_id}",
    "brief": "Create a single-page site that displays 'Hello World' with Bootstrap 5, sets the page title to 'Test App', and shows the current date inside an element with id='current-date'.",
    "checks": [
        "Page uses Bootstrap 5 from CDN",
        "Page title is 'Test App'",
        "Element with id='current-date' exists and shows a date"
    ],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
}

print("="*60)
print("Sending test request to http://localhost:5000/api-endpoint")
print("="*60)
print(f"📧 Email: {payload['email']}")
print(f"🎯 Task: {payload['task']}")
print(f"📝 Brief: {payload['brief'][:80]}...")
print(f"\n⏳ Waiting for response (this may take 1-2 minutes)...\n")

try:
    response = requests.post(
        'http://localhost:5000/api-endpoint',
        json=payload,
        headers={'Content-Type': 'application/json'},
        timeout=300  # 5 minutes timeout
    )
    
    print("="*60)
    print(f"✅ Response received!")
    print("="*60)
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        result = response.json()
        print("\n" + "="*60)
        print("🎉 SUCCESS! App created and deployed!")
        print("="*60)
        print(f"📦 GitHub Repo: {result.get('repo_url')}")
        print(f"🌐 Live Site: {result.get('pages_url')}")
        print(f"\n💡 Open the live site in your browser to see the app!")
        print("="*60)
    
except requests.exceptions.Timeout:
    print("❌ Request timed out (took longer than 5 minutes)")
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to server. Is it running at http://localhost:5000?")
except Exception as e:
    print(f"❌ Error: {e}")
