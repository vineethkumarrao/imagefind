"""
API Endpoint Test Script
Tests all backend endpoints to verify functionality
"""

import requests
import json
from pathlib import Path
from PIL import Image
import io

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Health check passed: {data}")
            return True
        else:
            print(f"  ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print("\n🔍 Testing / endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Root endpoint: {data}")
            return True
        else:
            print(f"  ❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_stats():
    """Test stats endpoint"""
    print("\n🔍 Testing /api/stats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Stats retrieved:")
            print(f"     - Success: {data.get('success')}")
            stats = data.get('statistics', {})
            print(f"     - Dimension: {stats.get('dimension')}")
            print(f"     - Total vectors: {stats.get('total_vector_count', 0)}")
            return True
        else:
            print(f"  ❌ Stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def create_test_image():
    """Create a test image"""
    img = Image.new('RGB', (224, 224), color='blue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_upload():
    """Test upload endpoint (search only)"""
    print("\n🔍 Testing /api/upload endpoint (search only)...")
    try:
        # Create test image
        test_image = create_test_image()
        
        # Upload
        files = {'file': ('test_image.jpg', test_image, 'image/jpeg')}
        response = requests.post(f"{BASE_URL}/api/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Upload successful:")
            print(f"     - Success: {data.get('success')}")
            print(f"     - Similar images found: {len(data.get('similar_images', []))}")
            
            # Show first result if available
            if data.get('similar_images'):
                first = data['similar_images'][0]
                print(f"     - Top match: {first.get('filename')} ({first.get('similarity'):.3f})")
            
            return True
        else:
            print(f"  ❌ Upload failed: {response.status_code}")
            print(f"     Response: {response.text}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_upload_and_store():
    """Test upload-and-store endpoint"""
    print("\n🔍 Testing /api/upload-and-store endpoint...")
    try:
        # Create test image
        test_image = create_test_image()
        
        # Upload and store
        files = {'file': ('test_store_image.jpg', test_image, 'image/jpeg')}
        data = {'category': 'healthcare'}
        response = requests.post(f"{BASE_URL}/api/upload-and-store", files=files, data=data)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Upload & store successful:")
            print(f"     - Success: {data.get('success')}")
            
            uploaded = data.get('uploaded_image', {})
            print(f"     - Uploaded: {uploaded.get('filename')}")
            print(f"     - URL: {uploaded.get('cloudinary_url', '')[:50]}...")
            
            print(f"     - Similar images found: {len(data.get('similar_images', []))}")
            
            return True
        else:
            print(f"  ❌ Upload & store failed: {response.status_code}")
            print(f"     Response: {response.text}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_api_tests():
    """Run all API tests"""
    print("="*60)
    print("🚀 API ENDPOINT FUNCTIONALITY TEST")
    print("="*60)
    
    # Check if server is running
    print("\n📡 Checking if backend server is running...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        print("✅ Backend server is running!\n")
    except Exception as e:
        print(f"❌ Backend server is not running or not accessible!")
        print(f"   Please start the backend server first.")
        print(f"   Error: {e}")
        return False
    
    results = {
        'health': test_health(),
        'root': test_root(),
        'stats': test_stats(),
        'upload': test_upload(),
        'upload_and_store': test_upload_and_store()
    }
    
    print("\n" + "="*60)
    print("📊 API TEST SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"TOTAL: {passed}/{total} API tests passed")
    
    if passed == total:
        print("\n🎉 ALL API TESTS PASSED! Backend is fully functional!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return False

if __name__ == '__main__':
    import sys
    success = run_api_tests()
    sys.exit(0 if success else 1)
