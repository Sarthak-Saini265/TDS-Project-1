"""
Send a Round 2 update request
"""
import requests
import json

# Use the SAME task name from Round 1
task_name = "test-app-20251013-160339-2474"  # UPDATE THIS with your actual task name

payload = {
    "email": "student@example.com",
    "secret": "geralt_of_rivia",
    "task": task_name,
    "round": 2,  # This is Round 2!
    "nonce": "test-nonce-round2-12345",
    "brief": "Add a button with id='click-me' that shows an alert saying 'Button clicked!' when clicked. Also change the background color to light blue.",
    "checks": [
        "Page has a button with id='click-me'",
        "Button shows alert when clicked",
        "Background color is light blue"
    ],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
}

print("="*60)
print("Sending Round 2 UPDATE request")
print("="*60)
print(f"🎯 Task: {payload['task']}")
print(f"🔄 Round: 2")
print(f"📝 Update: {payload['brief'][:80]}...")
print(f"\n⏳ Waiting for response...\n")

try:
    response = requests.post(
        'http://localhost:5000/api-endpoint',
        json=payload,
        headers={'Content-Type': 'application/json'},
        timeout=300
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
        print("🎉 SUCCESS! App updated!")
        print("="*60)
        print(f"📦 GitHub Repo: {result.get('repo_url')}")
        print(f"🌐 Live Site: {result.get('pages_url')}")
        print(f"\n💡 Refresh the site to see the updates!")
        print("="*60)
    
except Exception as e:
    print(f"❌ Error: {e}")
