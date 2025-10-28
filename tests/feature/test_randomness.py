"""Test if feature extraction has randomness"""
from unified_feature_extractor import UnifiedFeatureExtractor
from PIL import Image
import numpy as np

print("Testing feature extraction randomness...")

# Extract features 5 times
img = Image.open('testingimages/xray/NORMAL2-IM-0350-0001.jpeg')

results = []
for i in range(5):
    print(f"\nExtraction #{i+1}:")
    extractor = UnifiedFeatureExtractor(feature_dim=512)
    features = extractor.extract_features(img)
    results.append(features)
    print(f"  First 5 values: {features[:5]}")
    print(f"  Norm: {np.linalg.norm(features):.6f}")

# Compare all results
print(f"\n{'='*60}")
print("Comparing all extractions:")
for i in range(1, 5):
    sim = np.dot(results[0], results[i])
    match = "✅" if sim > 0.99 else "❌"
    print(f"  Extraction 1 vs {i+1}: {sim:.6f} {match}")
