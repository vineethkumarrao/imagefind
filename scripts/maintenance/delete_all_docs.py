"""Delete ALL documents from database"""
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval
from config import config

print("Deleting all documents from database...")
retrieval = AppwriteQuantumRetrieval()

# Get all documents
result = retrieval.databases.list_documents(
    config.APPWRITE_DATABASE_ID,
    config.APPWRITE_COLLECTION_ID
)

docs = result['documents']
print(f"\nFound {len(docs)} documents to delete...")

# Delete each document
deleted = 0
for doc in docs:
    try:
        retrieval.databases.delete_document(
            config.APPWRITE_DATABASE_ID,
            config.APPWRITE_COLLECTION_ID,
            doc['$id']
        )
        deleted += 1
        print(f"  ✅ Deleted: {doc['filename']} ({deleted}/{len(docs)})")
    except Exception as e:
        print(f"  ❌ Failed to delete {doc['filename']}: {e}")

print(f"\n✅ Successfully deleted {deleted}/{len(docs)} documents")
