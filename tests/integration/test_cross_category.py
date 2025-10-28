"""
Test cross-category similarity - verify different categories have lower similarity
"""
from unified_feature_extractor import UnifiedFeatureExtractor
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval
from src.quantum.ae_qip_algorithm import AEQIPAlgorithm
from PIL import Image
from config import config
import numpy as np

print("=" * 70)
print("🔍 CROSS-CATEGORY SIMILARITY TEST")
print("=" * 70)

# Initialize
extractor = UnifiedFeatureExtractor(feature_dim=2048)
retrieval = AppwriteQuantumRetrieval()
quantum_algo = AEQIPAlgorithm(use_quantum_inspired=True)

# Test 1: X-ray image
print("\n📸 Test 1: Uploading X-ray image...")
xray_img = Image.open('testingimages/xray/NORMAL2-IM-0350-0001.jpeg')
xray_features = extractor.extract_features(xray_img)

# Test 2: Surveillance image
print("📸 Test 2: Uploading surveillance image...")
survey_img = Image.open('testingimages/survey/000add18-e358-11ea-bb29-5e73ea6d71d7_jpg.rf.6809d4526b0e6e2c0134b9ec8b38f982.jpg')
survey_features = extractor.extract_features(survey_img)

# Calculate similarity between different categories
cross_similarity = quantum_algo.calculate_similarity(xray_features, survey_features)

print(f"\n{'='*70}")
print("📊 RESULTS:")
print(f"{'='*70}")
print(f"X-ray vs Surveillance similarity: {cross_similarity:.6f} ({cross_similarity*100:.2f}%)")

if cross_similarity < 0.60:
    print("✅ GOOD: Different categories have LOW similarity (<60%)")
elif cross_similarity < 0.80:
    print("⚠️  MODERATE: Different categories have MEDIUM similarity (60-80%)")
else:
    print("❌ BAD: Different categories have HIGH similarity (>80%)")
    print("   This suggests the model can't distinguish categories well")

# Get top matches for X-ray
print(f"\n{'='*70}")
print("🔍 Top matches for X-ray image:")
print(f"{'='*70}")

result = retrieval.databases.list_documents(
    config.APPWRITE_DATABASE_ID,
    config.APPWRITE_COLLECTION_ID
)

similarities = []
for doc in result['documents']:
    db_features = doc['features']
    similarity = quantum_algo.calculate_similarity(xray_features, db_features)
    similarities.append({
        'filename': doc['filename'],
        'category': doc['category'],
        'similarity': similarity
    })

similarities.sort(key=lambda x: x['similarity'], reverse=True)

print("\nTop 5 matches:")
for i, match in enumerate(similarities[:5], 1):
    category_icon = "🏥" if match['category'] == 'healthcare' else "📹"
    print(f"{i}. {category_icon} [{match['category']:12}] {match['filename'][:50]}")
    print(f"   Similarity: {match['similarity']:.6f} ({match['similarity']*100:.2f}%)")

# Count categories in top 10
healthcare_count = sum(1 for m in similarities[:10] if m['category'] == 'healthcare')
surveillance_count = sum(1 for m in similarities[:10] if m['category'] == 'surveillance')

print(f"\n{'='*70}")
print("📈 Top 10 Results Breakdown:")
print(f"{'='*70}")
print(f"🏥 Healthcare: {healthcare_count}/10")
print(f"📹 Surveillance: {surveillance_count}/10")

if healthcare_count >= 8:
    print("\n✅ EXCELLENT: X-ray query returns mostly healthcare images!")
elif healthcare_count >= 5:
    print("\n✅ GOOD: X-ray query prefers healthcare images")
else:
    print("\n⚠️  WARNING: X-ray query not distinguishing categories well")

print(f"\n{'='*70}")
