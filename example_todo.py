"""
Build a todo list app
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
    "task": f"todo-list-{timestamp}-{random_id}",
    "round": 1,
    "nonce": f"nonce-{random_id}",
    "brief": "Create a todo list app with Bootstrap 5. Users should be able to add tasks via an input field with id='task-input', display them in a list with id='task-list', mark tasks as complete by clicking them (add strikethrough), and delete tasks with a delete button. Store tasks in localStorage so they persist on page reload.",
    "checks": [
        "Page uses Bootstrap 5",
        "Has input field with id='task-input'",
        "Has task list with id='task-list'",
        "Can add new tasks",
        "Can mark tasks as complete",
        "Can delete tasks",
        "Uses localStorage for persistence"
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
