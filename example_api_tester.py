"""
Build a Postman-like API testing app
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
    "task": f"api-tester-{timestamp}-{random_id}",
    "round": 1,
    "nonce": f"nonce-{random_id}",
    "brief": """Create a beautiful Postman-like API testing tool with Bootstrap 5. 

Features required:
- URL input field with id='api-url' for entering the API endpoint
- Method selector dropdown with id='request-method' (GET, POST, PUT, DELETE)
- Request headers textarea with id='request-headers' (JSON format)
- Request body textarea with id='request-body' (for POST/PUT requests)
- Send button with id='send-button'
- Response section with id='response-section' that shows:
  - Status code with id='status-code'
  - Response time with id='response-time'
  - Response headers with id='response-headers' (formatted nicely)
  - Response body with id='response-body' (formatted JSON if applicable)
- Loading spinner that shows while request is in progress
- Error handling for invalid URLs or failed requests
- Copy response button to copy the response to clipboard
- Use syntax highlighting for JSON responses (can use highlight.js from CDN)
- Make it modern, colorful, and professional looking
- Add example API URL (like https://jsonplaceholder.typicode.com/posts/1) as placeholder
- Support CORS-enabled APIs (explain CORS limitations in the UI)

Make it look like a real API testing tool with tabs, proper spacing, and a clean interface.""",
    "checks": [
        "Page uses Bootstrap 5",
        "Has URL input with id='api-url'",
        "Has method selector with id='request-method'",
        "Has headers textarea with id='request-headers'",
        "Has body textarea with id='request-body'",
        "Has send button with id='send-button'",
        "Has response section with id='response-section'",
        "Has status code display with id='status-code'",
        "Has response time display with id='response-time'",
        "Has response headers display with id='response-headers'",
        "Has response body display with id='response-body'",
        "Can send GET requests",
        "Can send POST requests",
        "Displays response correctly",
        "Has loading state while fetching",
        "Has error handling"
    ],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
}

print("="*70)
print("🚀 Building Postman-like API Testing Tool")
print("="*70)
print(f"📦 Task: {payload['task']}")
print(f"📝 Features: URL input, method selector, headers, body, send button")
print(f"           response display with syntax highlighting")
print(f"\n⏳ Generating and deploying (this may take 1-2 minutes)...\n")

try:
    response = requests.post(
        'http://localhost:5000/api-endpoint',
        json=payload,
        headers={'Content-Type': 'application/json'},
        timeout=300
    )

    print("="*70)
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS! API Tester created and deployed!")
        print("="*70)
        print(f"📦 GitHub Repo: {result.get('repo_url')}")
        print(f"🌐 Live Site:   {result.get('pages_url')}")
        print("\n" + "="*70)
        print("💡 Try testing these APIs:")
        print("   - https://jsonplaceholder.typicode.com/posts/1 (GET)")
        print("   - https://httpbin.org/get (GET)")
        print("   - https://httpbin.org/post (POST)")
        print("="*70)
    else:
        print(f"❌ Error: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
except requests.exceptions.Timeout:
    print("❌ Request timed out (took longer than 5 minutes)")
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to server. Is it running at http://localhost:5000?")
except Exception as e:
    print(f"❌ Error: {e}")
