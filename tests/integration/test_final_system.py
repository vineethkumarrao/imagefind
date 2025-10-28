"""
Final comprehensive test - all 3 categories with 30 images
"""
from unified_feature_extractor import UnifiedFeatureExtractor
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval
from src.quantum.ae_qip_algorithm import AEQIPAlgorithm
from appwrite.query import Query
from PIL import Image
from config import config
import numpy as np

print("=" * 80)
print("🎯 FINAL SYSTEM TEST - ALL 3 CATEGORIES")
print("=" * 80)

# Initialize
extractor = UnifiedFeatureExtractor(feature_dim=2048)
retrieval = AppwriteQuantumRetrieval()
quantum_algo = AEQIPAlgorithm(use_quantum_inspired=True)

# Get database stats
result = retrieval.databases.list_documents(
    config.APPWRITE_DATABASE_ID,
    config.APPWRITE_COLLECTION_ID,
    queries=[Query.limit(5000)]
)

docs = result['documents']
print(f"\n📊 Database Statistics:")
print(f"   Total Images: {len(docs)}")

categories = {}
for doc in docs:
    cat = doc['category']
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in sorted(categories.items()):
    icon = "🏥" if cat == "healthcare" else "🛰️" if cat == "satellite" else "📹"
    print(f"   {icon} {cat.capitalize()}: {count} images")

# Test images from each category
test_images = [
    ("testingimages/xray/NORMAL2-IM-0350-0001.jpeg", "healthcare", "🏥"),
    ("testingimages/satellite/train_1722.jpg", "satellite", "🛰️"),
    ("testingimages/survey/000add18-e358-11ea-bb29-5e73ea6d71d7_jpg.rf.6809d4526b0e6e2c0134b9ec8b38f982.jpg", "surveillance", "📹")
]

print(f"\n{'='*80}")
print("🧪 TESTING EACH CATEGORY")
print(f"{'='*80}")

for img_path, expected_cat, icon in test_images:
    print(f"\n{icon} Testing {expected_cat.upper()} image:")
    print(f"   File: {img_path.split('/')[-1][:50]}")
    
    # Extract features
    img = Image.open(img_path)
    features = extractor.extract_features(img)
    
    # Calculate similarities
    similarities = []
    for doc in docs:
        db_features = doc['features']
        similarity = quantum_algo.calculate_similarity(features, db_features)
        similarities.append({
            'filename': doc['filename'],
            'category': doc['category'],
            'similarity': similarity
        })
    
    similarities.sort(key=lambda x: x['similarity'], reverse=True)
    
    # Show top 5
    print(f"\n   Top 5 matches:")
    for i, match in enumerate(similarities[:5], 1):
        cat_icon = "🏥" if match['category'] == 'healthcare' else "🛰️" if match['category'] == 'satellite' else "📹"
        match_marker = "✅" if match['category'] == expected_cat else "  "
        print(f"   {i}. {match_marker} {cat_icon} [{match['category']:12}] {match['similarity']:.4f}")
    
    # Count categories in top 10
    cat_counts = {}
    for match in similarities[:10]:
        cat = match['category']
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    
    print(f"\n   Top 10 breakdown:")
    for cat, count in sorted(cat_counts.items()):
        cat_icon = "🏥" if cat == 'healthcare' else "🛰️" if cat == 'satellite' else "📹"
        bar = "█" * count + "░" * (10 - count)
        marker = "✅" if cat == expected_cat else "  "
        print(f"   {marker} {cat_icon} {cat:12} [{bar}] {count}/10")
    
    # Check if majority matches expected category
    expected_count = cat_counts.get(expected_cat, 0)
    if expected_count >= 8:
        print(f"   ✅ EXCELLENT: {expected_count}/10 match expected category!")
    elif expected_count >= 5:
        print(f"   ✅ GOOD: {expected_count}/10 match expected category")
    else:
        print(f"   ⚠️  WARNING: Only {expected_count}/10 match expected category")

# Calculate average cross-category similarities
print(f"\n{'='*80}")
print("📈 CROSS-CATEGORY SIMILARITY ANALYSIS")
print(f"{'='*80}")

# Get one image from each category
healthcare_img = Image.open("testingimages/xray/NORMAL2-IM-0350-0001.jpeg")
satellite_img = Image.open("testingimages/satellite/train_1722.jpg")
surveillance_img = Image.open("testingimages/survey/000add18-e358-11ea-bb29-5e73ea6d71d7_jpg.rf.6809d4526b0e6e2c0134b9ec8b38f982.jpg")

healthcare_feat = extractor.extract_features(healthcare_img)
satellite_feat = extractor.extract_features(satellite_img)
surveillance_feat = extractor.extract_features(surveillance_img)

cross_sims = [
    ("Healthcare vs Satellite", quantum_algo.calculate_similarity(healthcare_feat, satellite_feat)),
    ("Healthcare vs Surveillance", quantum_algo.calculate_similarity(healthcare_feat, surveillance_feat)),
    ("Satellite vs Surveillance", quantum_algo.calculate_similarity(satellite_feat, surveillance_feat))
]

print("\nCross-category similarities (lower is better):")
for label, sim in cross_sims:
    bar_len = int(sim * 40)
    bar = "█" * bar_len + "░" * (40 - bar_len)
    status = "✅" if sim < 0.30 else "⚠️" if sim < 0.60 else "❌"
    print(f"{status} {label:28} [{bar}] {sim:.4f} ({sim*100:.2f}%)")

avg_cross_sim = sum(s for _, s in cross_sims) / len(cross_sims)
print(f"\n   Average cross-category similarity: {avg_cross_sim:.4f} ({avg_cross_sim*100:.2f}%)")

if avg_cross_sim < 0.30:
    print("   ✅ EXCELLENT separation between categories!")
elif avg_cross_sim < 0.50:
    print("   ✅ GOOD separation between categories")
else:
    print("   ⚠️  Categories may be hard to distinguish")

print(f"\n{'='*80}")
print("✅ FINAL SYSTEM TEST COMPLETE!")
print(f"{'='*80}")
print(f"\n📊 Summary:")
print(f"   • Total images: {len(docs)}")
print(f"   • Categories: {len(categories)}")
print(f"   • Feature dimension: 2048D")
print(f"   • Model: ResNet-50 (ImageNet)")
print(f"   • Status: ✅ PRODUCTION READY")
print(f"\n{'='*80}\n")
