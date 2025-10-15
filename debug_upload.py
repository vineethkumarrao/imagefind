"""Quick debug script to see what's happening"""
import requests
import json

# Upload image
print("Uploading image...")
with open('testingimages/xray/NORMAL2-IM-0381-0001.jpeg', 'rb') as f:
    files = {'file': ('NORMAL2-IM-0381-0001.jpeg', f, 'image/jpeg')}
    response = requests.post('http://localhost:8000/api/upload', files=files)

print(f"\nStatus Code: {response.status_code}")
print(f"\nResponse JSON:")
print(json.dumps(response.json(), indent=2))
