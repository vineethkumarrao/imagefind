"""Check database contents"""
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval
from config import config

r = AppwriteQuantumRetrieval()
result = r.databases.list_documents(
    config.APPWRITE_DATABASE_ID,
    config.APPWRITE_COLLECTION_ID
)

print(f"Total images in database: {result['total']}")
print(f"\nFirst 5 images:")
for i, doc in enumerate(result['documents'][:5], 1):
    print(f"{i}. {doc['filename']}")
    print(f"   - Features: {len(doc['features'])}D")
    print(f"   - Category: {doc['category']}")
