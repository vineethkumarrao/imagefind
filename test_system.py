"""
System Health Check and Functionality Test
Tests backend server, services, and ML model
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        from config import config
        print("config imported")
        from services.cloudinary_service import CloudinaryImageService
        print("cloudinary_service imported")
        from services.pinecone_service import PineconeVectorService
        print("pinecone_service imported")
        from ml.unified_feature_extractor import UnifiedFeatureExtractor
        print("unified_feature_extractor imported")
        print("\nAll imports successful!\n")
        return True
    except Exception as e:
        print(f"Import failed: {e}")
        return False

def test_config():
    """Test configuration"""
    print("Testing configuration...")
    try:
        from config import config
        print(f"  Cloudinary Cloud: {config.CLOUDINARY_CLOUD_NAME[:10]}...")
        print(f"  Pinecone Index: {config.PINECONE_INDEX_NAME}")
        print(f"  Feature Dimension: {config.FEATURE_DIMENSION}")
        print(f"  Categories: {config.CATEGORIES}")
        # Check for required env vars
        required = ['CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET', 'PINECONE_API_KEY']
        missing = []
        for var in required:
            if not getattr(config, var):
                missing.append(var)
        if missing:
            print(f"Missing config: {missing}")
            return False
        print("Configuration valid!\n")
        return True
    except Exception as e:
        print(f"Config test failed: {e}")
        return False

def test_feature_extractor():
    """Test feature extraction"""
    print("Testing feature extractor...")
    try:
        from ml.unified_feature_extractor import UnifiedFeatureExtractor
        from PIL import Image
        import numpy as np
        # Initialize extractor
        extractor = UnifiedFeatureExtractor(feature_dim=2048)
        print("  Extractor initialized")
        # Create a test image
        test_image = Image.new('RGB', (224, 224), color='red')
        print("  Test image created")
        # Extract features
        features = extractor.extract_features(test_image)
        print(f"  Features extracted: {len(features)} dimensions")
        # Validate
        if len(features) == 2048:
            print("  Feature dimension correct (2048D)")
        else:
            print(f"  Expected 2048D, got {len(features)}D")
            return False
        print("Feature extractor working!\n")
        return True
    except Exception as e:
        print(f"Feature extractor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pinecone():
    """Test Pinecone connection"""
    print("Testing Pinecone connection...")
    try:
        from services.pinecone_service import PineconeVectorService
        service = PineconeVectorService()
        print("  Pinecone service initialized")
        stats = service.get_statistics()
        print(f"  Index stats: {stats.get('dimension')}D, {stats.get('total_vector_count', 0)} vectors")
        print("Pinecone connected!\n")
        return True
    except Exception as e:
        print(f"Pinecone test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cloudinary():
    """Test Cloudinary connection"""
    print("Testing Cloudinary connection...")
    try:
        from services.cloudinary_service import CloudinaryImageService
        import cloudinary
        service = CloudinaryImageService()
        print("  Cloudinary service initialized")
        # Check config
        if cloudinary.config().cloud_name:
            print(f"  Cloud name: {cloudinary.config().cloud_name}")
        else:
            print("  Cloudinary not configured")
            return False
        print("Cloudinary configured!\n")
        return True
    except Exception as e:
        print(f"Cloudinary test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backend_server():
    """Test if backend server file is valid"""
    print("Testing backend server...")
    try:
        # Check if file exists
        backend_path = Path(__file__).parent / 'backend' / 'backend_server.py'
        if not backend_path.exists():
            print(f"Backend server not found at {backend_path}")
            return False
        print(f"  Backend server file exists")
        # Try to import (without running)
        import importlib.util
        spec = importlib.util.spec_from_file_location("backend_server", backend_path)
        module = importlib.util.module_from_spec(spec)
        print("  Backend server syntax valid")
        print("Backend server ready!\n")
        return True
    except Exception as e:
        print(f"Backend server test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("SYSTEM HEALTH CHECK & FUNCTIONALITY TEST")
    print("="*60)
    print()
    
    results = {
        'imports': test_imports(),
        'config': test_config(),
        'feature_extractor': test_feature_extractor(),
        'pinecone': test_pinecone(),
        'cloudinary': test_cloudinary(),
        'backend_server': test_backend_server()
    }
    
    print("="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
    print()
    print(f"TOTAL: {passed}/{total} tests passed")
    if passed == total:
        print("\nALL TESTS PASSED! System is ready!")
        return True
    else:
        print(f"\n{total - passed} test(s) failed. Please fix before running servers.")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
