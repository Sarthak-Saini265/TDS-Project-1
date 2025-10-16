"""
Test Round 2: Update an existing app
This demonstrates the revision/update functionality
"""
import requests
import json
from datetime import datetime
import random

# STEP 1: Create a simple app first (Round 1)
print("="*70)
print("STEP 1: Creating initial app (Round 1)")
print("="*70)

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
random_id = random.randint(1000, 9999)
task_name = f"counter-app-{timestamp}-{random_id}"

round1_payload = {
    "email": "student@example.com",
    "secret": "geralt_of_rivia",
    "task": task_name,
    "round": 1,
    "nonce": f"nonce-round1-{random_id}",
    "brief": "Create a simple counter app with Bootstrap 5. It should have a display showing the count (starting at 0) with id='counter-display', an increment button with id='btn-increment', and a decrement button with id='btn-decrement'. Make it look clean and modern.",
    "checks": [
        "Page uses Bootstrap 5",
        "Has counter display with id='counter-display'",
        "Has increment button with id='btn-increment'",
        "Has decrement button with id='btn-decrement'",
        "Counter increases when increment is clicked",
        "Counter decreases when decrement is clicked"
    ],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
}

print(f"📦 Task: {task_name}")
print(f"📝 Creating: Simple counter app with +/- buttons")
print(f"\n⏳ Building Round 1...\n")

try:
    response1 = requests.post(
        'http://localhost:5000/api-endpoint',
        json=round1_payload,
        headers={'Content-Type': 'application/json'},
        timeout=300
    )
    
    if response1.status_code == 200:
        result1 = response1.json()
        print("✅ Round 1 SUCCESS!")
        print(f"📦 Repo: {result1.get('repo_url')}")
        print(f"🌐 Live: {result1.get('pages_url')}")
        
        # STEP 2: Now update the app (Round 2)
        print("\n" + "="*70)
        print("STEP 2: Updating the app with new features (Round 2)")
        print("="*70)
        
        # Wait a moment
        import time
        time.sleep(2)
        
        round2_payload = {
            "email": "student@example.com",
            "secret": "geralt_of_rivia",
            "task": task_name,  # SAME task name!
            "round": 2,  # This is Round 2!
            "nonce": f"nonce-round2-{random_id}",
            "brief": "Update the counter app: Add a RESET button with id='btn-reset' that sets the counter back to 0. Also add a DOUBLE button with id='btn-double' that doubles the current count. Change the background to a light gradient (blue to purple). Add a label showing 'Current Count:' before the number.",
            "checks": [
                "Page still uses Bootstrap 5",
                "Has all previous buttons (increment, decrement)",
                "Has NEW reset button with id='btn-reset'",
                "Has NEW double button with id='btn-double'",
                "Reset button sets counter to 0",
                "Double button multiplies counter by 2",
                "Background has gradient styling",
                "Has label text before the counter"
            ],
            "evaluation_url": "https://httpbin.org/post",
            "attachments": []
        }
        
        print(f"📦 Task: {task_name} (same task, updating)")
        print(f"📝 Adding: Reset button, Double button, gradient background, label")
        print(f"\n⏳ Updating (Round 2)...\n")
        
        response2 = requests.post(
            'http://localhost:5000/api-endpoint',
            json=round2_payload,
            headers={'Content-Type': 'application/json'},
            timeout=300
        )
        
        print("="*70)
        if response2.status_code == 200:
            result2 = response2.json()
            print("✅ Round 2 SUCCESS! App Updated!")
            print("="*70)
            print(f"📦 Repo: {result2.get('repo_url')}")
            print(f"🌐 Live: {result2.get('pages_url')}")
            print("\n" + "="*70)
            print("🎉 COMPLETE WORKFLOW DEMONSTRATED!")
            print("="*70)
            print("Round 1: Created basic counter with +/- buttons")
            print("Round 2: Added reset, double buttons & gradient background")
            print("\n💡 Visit the live site to see the updated app!")
            print("   Refresh the page if it's still cached")
            print("="*70)
        else:
            print(f"❌ Round 2 Error: {response2.status_code}")
            print(json.dumps(response2.json(), indent=2))
    else:
        print(f"❌ Round 1 Error: {response1.status_code}")
        print(json.dumps(response1.json(), indent=2))
        
except requests.exceptions.Timeout:
    print("❌ Request timed out")
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to server. Is it running at http://localhost:5000?")
except Exception as e:
    print(f"❌ Error: {e}")
