"""
Quick test uploader for Cloudinary + Pinecone
Upload sample images to test the system
"""

import os
import sys
from pathlib import Path
from PIL import Image
import io
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from services.cloudinary_service import CloudinaryImageService
from services.pinecone_service import PineconeVectorService
from unified_feature_extractor import UnifiedFeatureExtractor

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_upload_image(image_path: str, category: str):
    """Test upload to Cloudinary + Pinecone"""
    
    logger.info("=" * 60)
    logger.info(f"Testing upload: {image_path}")
    logger.info(f"Category: {category}")
    logger.info("=" * 60)
    
    # Initialize services
    logger.info("Initializing services...")
    cloudinary = CloudinaryImageService()
    pinecone = PineconeVectorService()
    extractor = UnifiedFeatureExtractor(feature_dim=config.FEATURE_DIMENSION)
    
    # Load image
    logger.info(f"Loading image: {image_path}")
    image = Image.open(image_path).convert('RGB')
    logger.info(f"Image size: {image.size}")
    
    # Extract features
    logger.info("Extracting features...")
    features = extractor.extract_features(image)
    logger.info(f"Features: {len(features)}D vector")
    
    # Read image bytes
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    filename = Path(image_path).name
    
    # Upload to Cloudinary
    logger.info("Uploading to Cloudinary...")
    result = cloudinary.upload_image(
        file_data=image_data,
        filename=filename,
        category=category
    )
    
    cloudinary_url = result['secure_url']
    public_id = result['public_id']
    
    logger.info(f"✅ Uploaded to Cloudinary!")
    logger.info(f"   URL: {cloudinary_url}")
    logger.info(f"   Public ID: {public_id}")
    logger.info(f"   Folder: quantum-images/{category}")
    
    # Index in Pinecone
    logger.info("Indexing in Pinecone...")
    vector_id = public_id.replace('/', '_')
    
    metadata = {
        'filename': filename,
        'category': category,
        'cloudinary_url': cloudinary_url,
        'cloudinary_public_id': public_id,
        'uploaded_at': datetime.utcnow().isoformat(),
        'format': result.get('format'),
        'width': result.get('width'),
        'height': result.get('height')
    }
    
    success = pinecone.upsert_vector(vector_id, features, metadata)
    
    if success:
        logger.info(f"✅ Indexed in Pinecone!")
        logger.info(f"   Vector ID: {vector_id}")
    
    # Search for similar
    logger.info("Searching for similar images...")
    matches = pinecone.search(
        query_features=features,
        top_k=5,
        category_filter=category,
        min_score=0.0
    )
    
    logger.info(f"Found {len(matches)} similar images:")
    for i, match in enumerate(matches, 1):
        logger.info(f"   {i}. {match['metadata'].get('filename')} - Similarity: {match['score']:.4f}")
    
    logger.info("\n✅ TEST COMPLETE!\n")
    return True


def main():
    """Test with sample images"""
    
    logger.info("\n" + "🧪 " * 20)
    logger.info("TESTING CLOUDINARY + PINECONE UPLOAD")
    logger.info("🧪 " * 20 + "\n")
    
    # Check if test images exist
    test_dirs = {
        'healthcare': 'testingimages/xray',
        'satellite': 'testingimages/satellite',
        'surveillance': 'testingimages/survey'
    }
    
    uploaded = 0
    for category, directory in test_dirs.items():
        dir_path = Path(directory)
        if dir_path.exists():
            images = list(dir_path.glob('*.jpg')) + list(dir_path.glob('*.png'))
            if images:
                # Upload first image from each category
                test_image = images[0]
                logger.info(f"\n📤 Testing {category} category with: {test_image.name}")
                try:
                    test_upload_image(str(test_image), category)
                    uploaded += 1
                except Exception as e:
                    logger.error(f"❌ Upload failed: {e}")
            else:
                logger.warning(f"⚠️  No images found in {directory}")
        else:
            logger.warning(f"⚠️  Directory not found: {directory}")
    
    logger.info("\n" + "=" * 60)
    logger.info(f"📊 SUMMARY: Uploaded {uploaded}/3 test images")
    logger.info("=" * 60)
    
    if uploaded > 0:
        logger.info("\n✅ Upload test successful!")
        logger.info("💡 Check Cloudinary dashboard to see your images")
        logger.info("💡 Check Pinecone dashboard to see indexed vectors")
    else:
        logger.error("\n❌ No images uploaded. Check test image directories.")


if __name__ == "__main__":
    main()
