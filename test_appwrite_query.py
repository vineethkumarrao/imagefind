"""
Test Appwrite query to debug the 'request cannot have request body' error
"""
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
from config import config
import logging

logging.basicConfig(level=logging.DEBUG)

# Initialize client
client = Client()
client.set_endpoint(config.APPWRITE_ENDPOINT)
client.set_project(config.APPWRITE_PROJECT_ID)
client.set_key(config.APPWRITE_API_KEY)

databases = Databases(client)

print("=" * 60)
print("Test 1: List documents WITHOUT queries")
print("=" * 60)
try:
    result = databases.list_documents(
        database_id=config.APPWRITE_DATABASE_ID,
        collection_id=config.APPWRITE_COLLECTION_ID
    )
    print(f"✅ SUCCESS: Found {result['total']} documents")
except Exception as e:
    print(f"❌ FAILED: {e}")

print("\n" + "=" * 60)
print("Test 2: List documents WITH empty queries list")
print("=" * 60)
try:
    result = databases.list_documents(
        database_id=config.APPWRITE_DATABASE_ID,
        collection_id=config.APPWRITE_COLLECTION_ID,
        queries=[]
    )
    print(f"✅ SUCCESS: Found {result['total']} documents")
except Exception as e:
    print(f"❌ FAILED: {e}")

print("\n" + "=" * 60)
print("Test 3: List documents WITH Query.limit(10)")
print("=" * 60)
try:
    result = databases.list_documents(
        database_id=config.APPWRITE_DATABASE_ID,
        collection_id=config.APPWRITE_COLLECTION_ID,
        queries=[Query.limit(10)]
    )
    print(f"✅ SUCCESS: Found {result['total']} documents")
except Exception as e:
    print(f"❌ FAILED: {e}")

print("\n" + "=" * 60)
print("Test 4: List documents WITH Query.equal() filter")
print("=" * 60)
try:
    result = databases.list_documents(
        database_id=config.APPWRITE_DATABASE_ID,
        collection_id=config.APPWRITE_COLLECTION_ID,
        queries=[Query.equal('category', 'healthcare')]
    )
    print(f"✅ SUCCESS: Found {result['total']} documents")
except Exception as e:
    print(f"❌ FAILED: {e}")

print("\n" + "=" * 60)
print("Test 5: List documents WITH Query.equal() + Query.limit()")
print("=" * 60)
try:
    result = databases.list_documents(
        database_id=config.APPWRITE_DATABASE_ID,
        collection_id=config.APPWRITE_COLLECTION_ID,
        queries=[
            Query.equal('category', 'healthcare'),
            Query.limit(5)
        ]
    )
    print(f"✅ SUCCESS: Found {result['total']} documents")
except Exception as e:
    print(f"❌ FAILED: {e}")
