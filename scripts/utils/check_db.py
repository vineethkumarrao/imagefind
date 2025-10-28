"""Check Pinecone database contents"""
from services.pinecone_service import PineconeVectorService

p = PineconeVectorService()
stats = p.get_statistics()

print(f"Total vectors in Pinecone: {stats.get('vectors', 0)}")
print(f"Dimension: {stats.get('dimension', 2048)}")
print(f"\nIndex Status: {stats.get('status', 'unknown')}")
