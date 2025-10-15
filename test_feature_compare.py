"""
Compare local features vs database features
"""
from unified_feature_extractor import UnifiedFeatureExtractor
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval
from PIL import Image
from config import config
import numpy as np

print("Comparing local vs database features...")

# Extract features locally
extractor = UnifiedFeatureExtractor(feature_dim=512)
img = Image.open('testingimages/xray/NORMAL2-IM-0350-0001.jpeg')
local_features = extractor.extract_features(img)

print(f"\n✅ Local features:")
print(f"   Dimension: {len(local_features)}")
print(f"   Norm: {np.linalg.norm(local_features):.6f}")
print(f"   Range: [{min(local_features):.6f}, {max(local_features):.6f}]")
print(f"   First 5 values: {local_features[:5]}")

# Get features from database
retrieval = AppwriteQuantumRetrieval()
result = retrieval.databases.list_documents(
    config.APPWRITE_DATABASE_ID,
    config.APPWRITE_COLLECTION_ID
)

# Find the matching document
db_features = None
for doc in result['documents']:
    if doc['filename'] == 'NORMAL2-IM-0350-0001.jpeg':
        db_features = doc['features']
        break

if db_features:
    print(f"\n📦 Database features:")
    print(f"   Dimension: {len(db_features)}")
    print(f"   Norm: {np.linalg.norm(db_features):.6f}")
    print(f"   Range: [{min(db_features):.6f}, {max(db_features):.6f}]")
    print(f"   First 5 values: {db_features[:5]}")
    
    # Calculate similarity
    cosine_sim = np.dot(local_features, db_features)
    print(f"\n📊 Cosine similarity: {cosine_sim:.6f}")
    
    if cosine_sim < 0.99:
        print(f"\n❌ FEATURES MISMATCH!")
        print(f"   The features in database are different from local extraction")
        print(f"   This explains why exact match has low similarity!")
    else:
        print(f"\n✅ Features match!")
else:
    print(f"\n❌ Document not found in database!")
