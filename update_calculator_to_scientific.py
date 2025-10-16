"""
Update existing calculator app to scientific calculator
Make sure to update the task name below with your actual calculator task name!
"""
import requests
import json

# ⚠️ IMPORTANT: Replace this with your actual calculator task name
# You can find it in the terminal output from when you created the calculator
# It will look something like: "calculator-app-20251013-161234-5678"
CALCULATOR_TASK_NAME = "calculator-app-20251013-161559-4081"  # ← UPDATE THIS!

# If you don't remember it, check your GitHub repos at:
# https://github.com/Sarthak-Saini265?tab=repositories
# Look for a repo starting with "calculator-app-"

print("="*70)
print("🔬 UPDATING CALCULATOR TO SCIENTIFIC CALCULATOR")
print("="*70)

# Round 2: Update to scientific calculator
round2_payload = {
    "email": "student@example.com",
    "secret": "geralt_of_rivia",
    "task": CALCULATOR_TASK_NAME,  # Same task name as the original calculator
    "round": 2,  # This is Round 2 - an update!
    "nonce": "scientific-calc-update-12345",
    "brief": """Update calculator to scientific calculator. Keep existing UI and add these buttons with their IDs:
- Square root (√): id='btn-sqrt' - calculates Math.sqrt()
- Square (x²): id='btn-square' - calculates number squared
- Sin: id='btn-sin' - calculates Math.sin() in radians
- Cos: id='btn-cos' - calculates Math.cos() in radians  
- Tan: id='btn-tan' - calculates Math.tan() in radians
- Pi (π): id='btn-pi' - inserts 3.14159
- Parentheses: id='btn-lparen' and id='btn-rparen' for ( and )

Add a second row or column for these scientific buttons. Keep all existing basic calculator buttons. Use Bootstrap grid to organize nicely.""",
    "checks": [
        "Page uses Bootstrap 5",
        "Has display field with id='display'",
        "Has all basic calculator buttons",
        "Has square root button with id='btn-sqrt'",
        "Has square button with id='btn-square'",
        "Has sin button with id='btn-sin'",
        "Has cos button with id='btn-cos'",
        "Has tan button with id='btn-tan'",
        "Has pi button with id='btn-pi'",
        "Has parentheses buttons with id='btn-lparen' and id='btn-rparen'",
        "Scientific functions work correctly"
    ],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
}

print(f"📦 Task: {CALCULATOR_TASK_NAME}")
print(f"🔧 Update: Adding scientific calculator features")
print(f"\n📝 Changes:")
print(f"   ✓ Keep existing UI and basic functions")
print(f"   ✓ Add sqrt, square, sin, cos, tan buttons")
print(f"   ✓ Add π (pi) and parentheses")
print(f"   ✓ Organize in clean layout")

# Check if task name was updated
if "YYYYMMDD" in CALCULATOR_TASK_NAME or "XXXX" in CALCULATOR_TASK_NAME:
    print("\n" + "="*70)
    print("⚠️  ERROR: You need to update the task name!")
    print("="*70)
    print("Open this script and change line 10 to your actual calculator task name.")
    print("\nTo find it:")
    print("1. Go to: https://github.com/Sarthak-Saini265?tab=repositories")
    print("2. Look for a repo starting with 'calculator-app-'")
    print("3. Copy the full repo name (e.g., 'calculator-app-20251013-161234-5678')")
    print("4. Update CALCULATOR_TASK_NAME in this script")
    print("5. Run the script again")
    print("="*70)
    exit(1)

print(f"\n⏳ Sending update request to API...\n")

try:
    response = requests.post(
        'http://localhost:5000/api-endpoint',
        json=round2_payload,
        headers={'Content-Type': 'application/json'},
        timeout=1000
    )
    
    print("="*70)
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS! Calculator Updated to Scientific Calculator!")
        print("="*70)
        print(f"📦 GitHub Repo: {result.get('repo_url')}")
        print(f"🌐 Live Site:   {result.get('pages_url')}")
        print("\n" + "="*70)
        print("🔍 CHECK THE UPDATES!")
        print("="*70)
        print("1. Open the live site (or refresh if already open)")
        print("2. Use Ctrl+F5 for hard refresh to clear cache")
        print("3. You should now see:")
        print("   ✓ All original calculator buttons still there")
        print("   ✓ NEW scientific function buttons")
        print("   ✓ Same beautiful UI maintained")
        print("   ✓ Better organized layout")
        print("4. Test the new scientific functions:")
        print("   • Try: 9 then √ (should show 3)")
        print("   • Try: 3 then x² (should show 9)")
        print("   • Try: sin(0) or cos(0)")
        print("   • Try: π (should show 3.14159...)")
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
