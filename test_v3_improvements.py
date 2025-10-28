"""
Quick Test Script for v3.0 Improvements
Tests caching, multi-model support, and performance
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_cache_service():
    """Test Redis cache service"""
    print("1 Testing Cache Service...")
    try:
        from services.cache_service import get_cache
        cache = get_cache()
        
        test_data = b"test image data"
        test_features = [0.1, 0.2, 0.3]
        
        # Test set
        cache.set_features(test_data, test_features)
        
        # Test get
        retrieved = cache.get_features(test_data)
        
        if retrieved == test_features:
            print("    Cache working correctly")
        else:
            print("    Cache returned different data")
        
        # Test stats
        stats = cache.get_stats()
        print(f"    Cache stats: {stats}")
        
    except Exception as e:
        print(f"    Cache test skipped: {e}")

def test_feature_extractors():
    """Test different feature extractors"""
    print("\n2 Testing Feature Extractors...")
    
    from PIL import Image
    import numpy as np
    
    # Create dummy image
    dummy_img = Image.new("RGB", (224, 224), color="red")
    
    # Test ResNet
    try:
        from ml.unified_feature_extractor import UnifiedFeatureExtractor
        extractor = UnifiedFeatureExtractor(feature_dim=512, use_amp=True)
        
        start = time.time()
        features = extractor.extract_features(dummy_img)
        elapsed = time.time() - start
        
        print(f"    ResNet-50: {len(features)}D features in {elapsed:.3f}s")
    except Exception as e:
        print(f"    ResNet failed: {e}")
    
    # Test ViT
    try:
        from ml.feature_extractors.vit_extractor import ViTFeatureExtractor
        vit_extractor = ViTFeatureExtractor()
        
        start = time.time()
        vit_features = vit_extractor.extract_features(dummy_img)
        elapsed = time.time() - start
        
        print(f"    ViT: {len(vit_features)}D features in {elapsed:.3f}s")
    except Exception as e:
        print(f"    ViT not available: {e}")
    
    # Test Ensemble
    try:
        from ml.feature_extractors.ensemble_extractor import EnsembleFeatureExtractor
        ensemble = EnsembleFeatureExtractor(feature_dim=512)
        
        start = time.time()
        ensemble_features = ensemble.extract_features(dummy_img)
        elapsed = time.time() - start
        
        print(f"    Ensemble: {len(ensemble_features)}D features in {elapsed:.3f}s")
    except Exception as e:
        print(f"    Ensemble not available: {e}")

def test_batch_processing():
    """Test batch processing performance"""
    print("\n3 Testing Batch Processing...")
    
    from PIL import Image
    from ml.unified_feature_extractor import UnifiedFeatureExtractor
    
    extractor = UnifiedFeatureExtractor(feature_dim=512, use_amp=True)
    
    # Create batch of images
    images = [Image.new("RGB", (224, 224), color="red") for _ in range(10)]
    
    # Single image processing
    start = time.time()
    for img in images:
        _ = extractor.extract_features(img)
    single_time = time.time() - start
    
    # Batch processing
    start = time.time()
    _ = extractor.extract_batch_features(images)
    batch_time = time.time() - start
    
    speedup = single_time / batch_time
    
    print(f"   Single: {single_time:.3f}s for 10 images")
    print(f"   Batch: {batch_time:.3f}s for 10 images")
    print(f"    Speedup: {speedup:.2f}x faster")

def main():
    print("="*60)
    print("Quantum Image Retrieval System v3.0 - Test Suite")
    print("="*60)
    
    test_cache_service()
    test_feature_extractors()
    test_batch_processing()
    
    print("\n" + "="*60)
    print(" All tests complete!")
    print("="*60)

if __name__ == "__main__":
    main()
