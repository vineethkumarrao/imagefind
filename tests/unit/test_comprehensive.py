"""
Final comprehensive test - shows exactly what's happening
"""
from unified_feature_extractor import UnifiedFeatureExtractor  
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval
from src.quantum.ae_qip_algorithm import AEQIPAlgorithm
from PIL import Image
from config import config
import numpy as np

print("=" * 70)
print("COMPREHENSIVE SIMILARITY TEST")
print("=" * 70)

# 1. Initialize
print("\n1. Initializing components...")
extractor = UnifiedFeatureExtractor(feature_dim=2048)
retrieval = AppwriteQuantumRetrieval()
quantum_algo = AEQIPAlgorithm(use_quantum_inspired=True)

# 2. Extract features from test image
print("\n2. Extracting features from test image...")
test_img = Image.open('testingimages/xray/NORMAL2-IM-0350-0001.jpeg')
test_features = extractor.extract_features(test_img)
print(f"   - Extracted {len(test_features)}D features")
print(f"   - Feature range: [{min(test_features):.4f}, {max(test_features):.4f}]")
print(f"   - Feature norm: {np.linalg.norm(test_features):.4f}")

# 3. Get documents from database
print("\n3. Fetching documents from database...")
result = retrieval.databases.list_documents(
    config.APPWRITE_DATABASE_ID,
    config.APPWRITE_COLLECTION_ID
)
docs = result['documents']
print(f"   - Found {len(docs)} documents")

# 4. Calculate similarities
print("\n4. Calculating similarities...")
similarities = []
for doc in docs:
    db_features = doc['features']
    similarity = quantum_algo.calculate_similarity(test_features, db_features)
    similarities.append({
        'filename': doc['filename'],
        'similarity': similarity
    })

# 5. Sort and display
similarities.sort(key=lambda x: x['similarity'], reverse=True)
print(f"\n5. Top 5 Results:")
for i, sim in enumerate(similarities[:5], 1):
    marker = "✅ EXACT MATCH!" if sim['filename'] == 'NORMAL2-IM-0350-0001.jpeg' else ""
    print(f"   {i}. {sim['filename']}: {sim['similarity']:.6f} {marker}")

# 6. Check if exact match is found
exact_match_pos = None
for i, sim in enumerate(similarities, 1):
    if sim['filename'] == 'NORMAL2-IM-0350-0001.jpeg':
        exact_match_pos = i
        exact_similarity = sim['similarity']
        break

print(f"\n6. Exact match check:")
if exact_match_pos:
    print(f"   ✅ Found at position #{exact_match_pos}")
    print(f"   Similarity: {exact_similarity:.6f} ({exact_similarity*100:.2f}%)")
    if exact_similarity >= 0.99:
        print(f"   ✅✅✅ PERFECT MATCH! (>99%)")
    elif exact_similarity >= 0.95:
        print(f"   ✅✅ EXCELLENT MATCH! (>95%)")
    elif exact_similarity >= 0.80:
        print(f"   ✅ GOOD MATCH (>80%)")
    else:
        print(f"   ⚠️ LOW SIMILARITY (<80%) - SOMETHING IS WRONG!")
else:
    print(f"   ❌ NOT FOUND in top {len(similarities)} results!")

print("\n" + "=" * 70)
