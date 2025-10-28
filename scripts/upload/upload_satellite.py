"""
Upload Satellite Images to Cloudinary and Pinecone
Extracts 2048D features using ResNet-50 and stores in Pinecone
"""

import time
from pathlib import Path
from PIL import Image
import logging

from config import config
from ml.unified_feature_extractor import UnifiedFeatureExtractor
from services.cloudinary_service import CloudinaryImageService
from services.pinecone_service import PineconeVectorService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def upload_satellite_images():
    """Upload all satellite images"""
    
    logger.info("="*70)
    logger.info("🛰️  SATELLITE IMAGES UPLOADER")
    logger.info("="*70)
    
    # Initialize
    logger.info("\nInitializing ResNet-50 feature extractor (2048D native)...")
    feature_extractor = UnifiedFeatureExtractor(feature_dim=2048, use_amp=True)
    
    logger.info("☁️ Connecting to Cloudinary...")
    cloudinary_service = CloudinaryImageService()
    
    logger.info("📊 Connecting to Pinecone...")
    pinecone_service = PineconeVectorService()
    
    # Setup paths
    images_folder = Path("data/testingimages/satellite")
    category = "satellite"
    
    if not images_folder.exists():
        logger.error(f"Folder not found: {images_folder}")
        return
    
    # Get image files
    image_files = list(images_folder.glob("*.jpg")) + \
    
    if not image_files:
        logger.error(f"No images found in {images_folder}")
        return
    
    logger.info(f"\nFound {len(image_files)} satellite images")
    logger.info(f"📁 Folder: {images_folder.absolute()}")
    logger.info(f"🛰️  Category: {category}")
    logger.info(" Model: ResNet-50 (2048D vectors)")
    
    # Upload images
    success = 0
    failed = 0
    start_time = time.time()
    
    for idx, image_path in enumerate(image_files, 1):
        try:
            logger.info(f"\n[{idx}/{len(image_files)}] {image_path.name}")
            
            # Load image
            image = Image.open(image_path).convert('RGB')
            logger.info(f"   📐 Size: {image.size}")
            
            # Extract 2048D features
            logger.info("   🧠 Extracting 2048D features...")
            features = feature_extractor.extract_features(image)
            logger.info(f"   Extracted 2048D vector")
            
            # Read image as bytes
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            # Upload to Cloudinary
            logger.info(f"   ☁️ Uploading to Cloudinary...")
            result = cloudinary_service.upload_image(
                image_bytes,
                image_path.name,
                category
            )
            
            # Store in Pinecone
            logger.info(f"   📊 Storing in Pinecone...")
            vector_id = result['public_id'].replace('/', '_')
            metadata = {
                'filename': image_path.name,
                'category': category,
                'cloudinary_url': result['secure_url']
            }
            pinecone_service.upsert_vector(vector_id, features, metadata)
            
            if result:
                success += 1
                public_id = result.get('public_id', 'N/A')[:8]
                logger.info(f"   SUCCESS - ID: {public_id}...")
            else:
                failed += 1
                logger.error("   Upload failed")
            
            time.sleep(0.3)
            
        except Exception as e:
            failed += 1
            logger.error(f"   Error: {e}")
    
    # Summary
    elapsed = time.time() - start_time
    avg_time = elapsed / max(len(image_files), 1)
    
    logger.info("\n" + "="*70)
    logger.info("SATELLITE UPLOAD SUMMARY")
    logger.info("="*70)
    logger.info(f"Successful: {success}")
    logger.info(f"Failed: {failed}")
    logger.info(f"📁 Total: {len(image_files)}")
    logger.info(f"⏱️  Time: {elapsed:.2f}s ({avg_time:.2f}s per image)")
    logger.info("="*70)
    
    return success, failed


if __name__ == "__main__":
    try:
        config.validate()
        upload_satellite_images()
        logger.info("\n✅ Upload complete!")
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
