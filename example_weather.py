"""
Build a weather dashboard (with mock data)
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
    "task": f"weather-dashboard-{timestamp}-{random_id}",
    "round": 1,
    "nonce": f"nonce-{random_id}",
    "brief": "Create a weather dashboard with Bootstrap 5. Show a search input with id='city-input' where users can enter a city name. Display weather cards showing temperature (id='temperature'), condition (id='condition'), humidity (id='humidity'), and wind speed (id='wind-speed'). Use mock data for demonstration - when user searches, show random weather data. Make it colorful and modern with weather icons.",
    "checks": [
        "Page uses Bootstrap 5",
        "Has search input with id='city-input'",
        "Has temperature display with id='temperature'",
        "Has condition display with id='condition'",
        "Has humidity display with id='humidity'",
        "Has wind speed display with id='wind-speed'",
        "Shows data when city is searched"
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
