"""
Build a brand new scientific calculator (instead of updating)
This avoids timeout issues with complex updates
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
    "task": f"scientific-calc-{timestamp}-{random_id}",
    "round": 1,
    "nonce": f"nonce-{random_id}",
    "brief": """Create a beautiful scientific calculator with Bootstrap 5.

DISPLAY:
- Input/display field with id='display' showing calculations

BASIC BUTTONS (0-9 and operations):
- Digits 0-9
- Operators: +, -, *, /
- Equals (=) and Clear (C) buttons

SCIENTIFIC BUTTONS:
- Square root (√) with id='btn-sqrt' 
- Square (x²) with id='btn-square'
- Sine with id='btn-sin'
- Cosine with id='btn-cos'  
- Tangent with id='btn-tan'
- Pi (π) with id='btn-pi'
- Left parenthesis with id='btn-lparen'
- Right parenthesis with id='btn-rparen'

DESIGN:
- Modern, colorful Bootstrap 5 design
- Organize basic numbers in a grid
- Scientific functions in a separate section or side panel
- Large, clickable buttons
- Professional calculator look
- Responsive layout

FUNCTIONALITY:
- All buttons work correctly
- Scientific functions use JavaScript Math library
- Handle expressions with eval() or similar
- Show results in display""",
    "checks": [
        "Page uses Bootstrap 5",
        "Has display with id='display'",
        "Has digits 0-9",
        "Has basic operators",
        "Has sqrt button with id='btn-sqrt'",
        "Has square button with id='btn-square'",
        "Has sin button with id='btn-sin'",
        "Has cos button with id='btn-cos'",
        "Has tan button with id='btn-tan'",
        "Has pi button with id='btn-pi'",
        "Has parentheses with id='btn-lparen' and id='btn-rparen'",
        "Calculator works correctly"
    ],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
}

print("="*70)
print("🔬 BUILDING NEW SCIENTIFIC CALCULATOR")
print("="*70)
print(f"📦 Task: {payload['task']}")
print(f"📝 Features: Basic + Scientific functions")
print(f"   ✓ Numbers and basic operations")
print(f"   ✓ √, x², sin, cos, tan")
print(f"   ✓ π and parentheses")
print(f"   ✓ Beautiful Bootstrap UI")
print(f"\n⏳ Building from scratch (faster than updating)...\n")

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
        print("✅ SUCCESS! Scientific Calculator Built!")
        print("="*70)
        print(f"📦 GitHub Repo: {result.get('repo_url')}")
        print(f"🌐 Live Site:   {result.get('pages_url')}")
        print("\n" + "="*70)
        print("🧪 TEST IT OUT!")
        print("="*70)
        print("Try these calculations:")
        print("  • 9 then √ button = 3")
        print("  • 3 then x² button = 9")
        print("  • sin(0) = 0")
        print("  • π button = 3.14159...")
        print("  • (2+3)*4 = 20")
        print("="*70)
    else:
        print(f"❌ Error: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
except requests.exceptions.Timeout:
    print("❌ Request timed out")
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to server. Is it running?")
except Exception as e:
    print(f"❌ Error: {e}")
