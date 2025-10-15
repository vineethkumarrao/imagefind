"""Test feature extraction consistency"""
from unified_feature_extractor import UnifiedFeatureExtractor
from PIL import Image
import numpy as np

print("Loading extractor...")
extractor = UnifiedFeatureExtractor(feature_dim=512)

print("Loading image...")
img = Image.open('testingimages/xray/NORMAL2-IM-0350-0001.jpeg')

print("Extracting features (first time)...")
features1 = extractor.extract_features(img)

print("Extracting features (second time)...")
features2 = extractor.extract_features(img)

print(f"\nFeature dimension: {len(features1)}")
print(f"Features match: {features1 == features2}")

if features1 != features2:
    f1 = np.array(features1)
    f2 = np.array(features2)
    diff = np.abs(f1 - f2)
    print(f"Max difference: {diff.max()}")
    print(f"Mean difference: {diff.mean()}")
else:
    print("✅ Features are identical!")
    
# Calculate similarity
from src.quantum.ae_qip_algorithm import AEQIPAlgorithm
algo = AEQIPAlgorithm(use_quantum_inspired=True)
similarity = algo.calculate_similarity(features1, features2)
print(f"\nSelf-similarity: {similarity:.6f}")
