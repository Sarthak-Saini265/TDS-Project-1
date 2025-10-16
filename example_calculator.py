"""
Build a calculator app
"""
import requests
import json
from datetime import datetime
import random

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
random_id = random.randint(1000, 9999)

payload = {
    "email": "student@example.com",
    "secret": "geralt_of_rivia",
    "task": f"calculator-app-{timestamp}-{random_id}",
    "round": 1,
    "nonce": f"nonce-{random_id}",
    "brief": "Create a beautiful calculator app with Bootstrap 5. It should have buttons for digits 0-9, operators (+, -, *, /), equals (=), and clear (C). Display the calculation in an input field with id='display'. Make it look modern and responsive.",
    "checks": [
        "Page uses Bootstrap 5",
        "Has input field with id='display'",
        "Has number buttons 0-9",
        "Has operator buttons",
        "Calculator works correctly"
    ],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
}

print(f"🎯 Building: {payload['brief'][:60]}...")
print(f"📦 Task: {payload['task']}\n")

response = requests.post(
    'http://localhost:5000/api-endpoint',
    json=payload,
    headers={'Content-Type': 'application/json'},
    timeout=300
)

if response.status_code == 200:
    result = response.json()
    print("✅ SUCCESS!")
    print(f"🌐 Live: {result.get('pages_url')}")
    print(f"📦 Repo: {result.get('repo_url')}")
else:
    print(f"❌ Error: {response.json()}")
