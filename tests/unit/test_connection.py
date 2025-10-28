"""Quick test for Cloudinary and Pinecone connections"""
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.api
from pinecone import Pinecone

# Load environment variables
load_dotenv()

print("=" * 60)
print("🧪 TESTING CLOUDINARY CONNECTION")
print("=" * 60)

try:
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )
    result = cloudinary.api.ping()
    print("✅ Cloudinary connected successfully!")
    print(f"Status: {result.get('status', 'OK')}")
except Exception as e:
    print(f"❌ Cloudinary error: {e}")

print("\n" + "=" * 60)
print("🌲 TESTING PINECONE CONNECTION")
print("=" * 60)

try:
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    indexes = pc.list_indexes()
    print("✅ Pinecone connected successfully!")
    print(f"Existing indexes: {[idx.name for idx in indexes]}")
except Exception as e:
    print(f"❌ Pinecone error: {e}")
    print("\n💡 Please verify your Pinecone API key at: https://app.pinecone.io/")
