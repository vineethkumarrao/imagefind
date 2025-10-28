"""Create .env file with proper formatting"""

env_content = """CLOUDINARY_CLOUD_NAME=ddyytqwbq
CLOUDINARY_API_KEY=315439667751671
CLOUDINARY_API_SECRET=J9F8TguFx9Xw9TgCyLAamS2jGF0
PINECONE_API_KEY=pcsk_6ymDQY_CpQG5yUj1BpjFYuD1g9KyuMFzebjbP1zvYXZ1v2jM7JLnevcgeLRbJTUGZxQqAM
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=quantum-images-prod
FEATURE_DIMENSION=2048
CATEGORIES=healthcare,satellite,surveillance
"""

with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content.strip())

print("✅ .env file created successfully!")

# Verify
from dotenv import load_dotenv
import os
load_dotenv()

print(f"\nCloud Name: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
print(f"API Key: {os.getenv('CLOUDINARY_API_KEY')}")
print(f"API Secret: {os.getenv('CLOUDINARY_API_SECRET')[:10]}...")
print(f"Pinecone: {os.getenv('PINECONE_API_KEY')[:20]}...")
