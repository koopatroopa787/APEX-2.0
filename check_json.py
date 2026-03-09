import json
try:
    with open('e:/Anti-gravity/Microsoft_hackathon/apex-platform/frontend/package.json', 'r') as f:
        json.load(f)
    print("Valid JSON")
except Exception as e:
    print(f"Invalid JSON: {e}")
