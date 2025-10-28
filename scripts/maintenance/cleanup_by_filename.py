"""Keep only unique satellite images - remove duplicates by filename"""
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval
from appwrite.query import Query
from config import config

print("Cleaning up duplicate satellite images by filename...")
retrieval = AppwriteQuantumRetrieval()

# Get all documents (with high limit to get everything)
result = retrieval.databases.list_documents(
    config.APPWRITE_DATABASE_ID,
    config.APPWRITE_COLLECTION_ID,
    queries=[Query.limit(5000)]
)

# Find satellite images grouped by filename
satellite_by_name = {}
for doc in result['documents']:
    if doc['category'] == 'satellite':
        filename = doc['filename']
        if filename not in satellite_by_name:
            satellite_by_name[filename] = []
        satellite_by_name[filename].append(doc)

print(f"\nFound {len(satellite_by_name)} unique satellite filenames")

# Delete duplicates (keep first occurrence)
deleted_count = 0
for filename, docs in satellite_by_name.items():
    if len(docs) > 1:
        print(f"\n{filename}: {len(docs)} copies")
        # Keep first, delete rest
        for doc in docs[1:]:
            try:
                retrieval.databases.delete_document(
                    config.APPWRITE_DATABASE_ID,
                    config.APPWRITE_COLLECTION_ID,
                    doc['$id']
                )
                deleted_count += 1
                print(f"  ✅ Deleted duplicate copy")
            except Exception as e:
                print(f"  ❌ Failed: {e}")

print(f"\n✅ Deleted {deleted_count} duplicate images")

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
