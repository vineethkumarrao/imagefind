"""
Test image search accuracy by uploading a testing image
and verifying if the same image is returned with highest similarity
"""

import requests
import os
from pathlib import Path

# Test configuration
BACKEND_URL = "http://localhost:8000"
TEST_IMAGE_PATH = "testingimages/xray/NORMAL2-IM-0350-0001.jpeg"

def test_image_search():
    """Test if the exact same image is found with highest similarity"""
    
    print("=" * 70)
    print("🧪 TESTING IMAGE SEARCH ACCURACY")
    print("=" * 70)
    
    # Check if test image exists
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"❌ Test image not found: {TEST_IMAGE_PATH}")
        return False
    
    print(f"\n📸 Test image: {TEST_IMAGE_PATH}")
    test_filename = os.path.basename(TEST_IMAGE_PATH)
    print(f"   Expected to find: {test_filename}")
    
    # Upload image for search
    print(f"\n🔄 Uploading image to {BACKEND_URL}/api/upload...")
    
    try:
        with open(TEST_IMAGE_PATH, 'rb') as f:
            files = {'file': (test_filename, f, 'image/jpeg')}
            response = requests.post(f"{BACKEND_URL}/api/upload", files=files)
        
        if response.status_code != 200:
            print(f"❌ Upload failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        result = response.json()
        
        print("\n" + "=" * 70)
        print("📊 SEARCH RESULTS")
        print("=" * 70)
        
        print(f"\n✅ Status: {result.get('status', 'unknown')}")
        print(f"   Message: {result.get('message', 'N/A')}")
        print(f"   Total results: {result.get('total_results', 0)}")
        print(f"   High confidence: {result.get('high_confidence_results', 0)}")
        
        # Check for exact match
        exact_match = result.get('exact_match')
        if exact_match:
            print(f"\n🎯 EXACT MATCH FOUND!")
            print(f"   Filename: {exact_match['filename']}")
            print(f"   Similarity: {exact_match['similarity']:.4f} ({exact_match['similarity']*100:.2f}%)")
            print(f"   Category: {exact_match['category']}")
        
        # Show top 5 results
        results = result.get('results', [])
        if results:
            print(f"\n🔝 TOP 5 RESULTS:")
            print("-" * 70)
            for i, img in enumerate(results[:5]):
                match_indicator = "✅ MATCH!" if img['filename'] == test_filename else "   "
                similarity_pct = img['similarity'] * 100
                print(f"{i+1}. {match_indicator} {img['filename']}")
                print(f"   Similarity: {img['similarity']:.6f} ({similarity_pct:.4f}%)")
                print(f"   Category: {img['category']}")
                print()
        else:
            print("\n❌ NO RESULTS FOUND")
        
        # Verify accuracy
        print("\n" + "=" * 70)
        print("🎯 ACCURACY CHECK")
        print("=" * 70)
        
        if not results:
            print("❌ FAILED: No results returned")
            return False
        
        top_result = results[0]
        if top_result['filename'] == test_filename:
            print(f"✅ SUCCESS: Exact same image found as #1 result!")
            print(f"   Similarity: {top_result['similarity']:.6f} ({top_result['similarity']*100:.4f}%)")
            
            if top_result['similarity'] >= 0.99:
                print("   ✅ Perfect match (>99% similarity)")
            elif top_result['similarity'] >= 0.95:
                print("   ✅ Excellent match (>95% similarity)")
            elif top_result['similarity'] >= 0.90:
                print("   ⚠️  Good match (>90% similarity)")
            else:
                print("   ⚠️  Moderate match (<90% similarity)")
            
            return True
        else:
            print(f"❌ FAILED: Expected '{test_filename}' but got '{top_result['filename']}'")
            print(f"   Top result similarity: {top_result['similarity']:.6f}")
            
            # Check if expected image is in top 10
            for i, img in enumerate(results):
                if img['filename'] == test_filename:
                    print(f"   ⚠️  Expected image found at position #{i+1}")
                    print(f"   Similarity: {img['similarity']:.6f}")
                    break
            else:
                print(f"   ❌ Expected image NOT found in top {len(results)} results")
            
            return False
    
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed: Is the backend server running on {BACKEND_URL}?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_image_search()
    print("\n" + "=" * 70)
    if success:
        print("✅ TEST PASSED: Image search working correctly!")
    else:
        print("❌ TEST FAILED: Image search needs improvement")
    print("=" * 70)
    
    exit(0 if success else 1)
