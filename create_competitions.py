
import requests
from datetime import datetime
import traceback

url = "http://127.0.0.1:8001/competitions/"
headers = {"Content-Type": "application/json"}

payload_template = {
    "name": "Competition {i}",
    "author": "admin",
    "date_created": datetime.now().isoformat(),
    "logo_location": None,
    "is_private": False,
    "type": "league",
    "rules": [
        {"name": "Rule 1", "description": "Sample rule"}
    ],
    "scoring_categories": [
        {"name": "Category 1", "description": "Sample category", "points": 1}
    ],
    "point_accumulation": {"win": 3, "lose": 0, "draw": 1},
    "participants": ["participant1"],
    "fixtures": ["fixture1"],
    "league_table": ["table1"],
    "posts": ["post1"],
    "photos": ["photo1"],
    "videos": ["video1"]
}

for i in range(1, 51):
    payload = payload_template.copy()
    payload["name"] = f"Competition {i}"
    payload["date_created"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Created Competition {i}: Status {response.status_code}")
        print("Response:", response.text)
        if response.status_code != 200:
            print("Error details:", response.json() if response.headers.get('content-type') == 'application/json' else response.text)
    except Exception as e:
        print(f"Failed to create Competition {i}: {e}")
        traceback.print_exc()
