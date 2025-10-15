"""
Delete ALL documents from Appwrite database
"""
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval
from config import config
from appwrite.query import Query

print("="*60)
print("DELETING ALL DOCUMENTS FROM DATABASE")
print("="*60)

retrieval = AppwriteQuantumRetrieval()

# Get all documents
result = retrieval.databases.list_documents(
    database_id=config.APPWRITE_DATABASE_ID,
    collection_id=config.APPWRITE_COLLECTION_ID,
    queries=[Query.limit(5000)]
)

documents = result['documents']
total = len(documents)

print(f"\n📊 Found {total} documents to delete")

if total == 0:
    print("✅ Database is already empty!")
else:
    confirm = input(f"\n⚠️  Delete ALL {total} documents? (yes/no): ")
    
    if confirm.lower() == 'yes':
        print("\n🗑️  Deleting documents...")
        
        for i, doc in enumerate(documents, 1):
            try:
                retrieval.databases.delete_document(
                    database_id=config.APPWRITE_DATABASE_ID,
                    collection_id=config.APPWRITE_COLLECTION_ID,
                    document_id=doc['$id']
                )
                print(f"  [{i}/{total}] Deleted: {doc['filename']}")
            except Exception as e:
                print(f"  [{i}/{total}] Error deleting {doc['filename']}: {e}")
        
        print(f"\n✅ Deleted {total} documents!")
    else:
        print("\n❌ Deletion cancelled")

print("="*60)
