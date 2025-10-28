"""Delete duplicate satellite images - keep only first 10"""
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval
from config import config

print("Removing duplicate satellite images...")
retrieval = AppwriteQuantumRetrieval()

# Get all documents
result = retrieval.databases.list_documents(
    config.APPWRITE_DATABASE_ID,
    config.APPWRITE_COLLECTION_ID
)

# Find satellite images
satellite_docs = [doc for doc in result['documents'] if doc['category'] == 'satellite']
print(f"\nFound {len(satellite_docs)} satellite images")

if len(satellite_docs) > 10:
    # Keep first 10, delete the rest
    to_keep = satellite_docs[:10]
    to_delete = satellite_docs[10:]
    
    print(f"Keeping first 10, deleting {len(to_delete)} duplicates...")
    
    deleted_count = 0
    for doc in to_delete:
        try:
            retrieval.databases.delete_document(
                config.APPWRITE_DATABASE_ID,
                config.APPWRITE_COLLECTION_ID,
                doc['$id']
            )
            deleted_count += 1
            print(f"  ✅ Deleted: {doc['filename']} ({deleted_count}/{len(to_delete)})")
        except Exception as e:
            print(f"  ❌ Failed: {doc['filename']} - {e}")
    
    print(f"\n✅ Cleanup complete! Deleted {deleted_count} duplicate satellite images")
else:
    print("✅ No duplicates found - database is clean!")

# Final count
result = retrieval.databases.list_documents(
    config.APPWRITE_DATABASE_ID,
    config.APPWRITE_COLLECTION_ID
)

categories = {}
for doc in result['documents']:
    cat = doc['category']
    categories[cat] = categories.get(cat, 0) + 1

print(f"\n📊 Final Database Status:")
print(f"   Total: {len(result['documents'])} images")
for cat, count in sorted(categories.items()):
    icon = "🏥" if cat == 'healthcare' else "🛰️" if cat == 'satellite' else "📹"
    print(f"   {icon} {cat.capitalize()}: {count}")
