"""
Upload Healthcare (X-ray) Images to Appwrite
Extracts 512D features using ResNet-50 and stores in healthcare-images bucket
"""

import os
import time
from pathlib import Path
from PIL import Image
import logging

from config import config
from unified_feature_extractor import UnifiedFeatureExtractor
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def upload_healthcare_images():
    """Upload all healthcare/x-ray images"""
    
    logger.info("="*70)
    logger.info("🏥 HEALTHCARE IMAGES UPLOADER")
    logger.info("="*70)
    
    # Initialize
    logger.info("\nInitializing ResNet-50 feature extractor (2048D native)...")
    feature_extractor = UnifiedFeatureExtractor(feature_dim=2048)
    
    logger.info(" Connecting to Appwrite...")
    retrieval = AppwriteQuantumRetrieval()
    
    # Setup paths
    images_folder = Path("testingimages/xray")
    category = "healthcare"
    bucket_id = "healthcare-images"
    
    if not images_folder.exists():
        logger.error(f"Folder not found: {images_folder}")
        return
    
    # Get image files
    image_files = list(images_folder.glob("*.jpeg")) + list(images_folder.glob("*.jpg"))
    
    if not image_files:
        logger.error(f"No images found in {images_folder}")
        return
    
    logger.info(f"\nFound {len(image_files)} healthcare images")
    logger.info(f"📁 Folder: {images_folder.absolute()}")
    logger.info(f"🏥 Category: {category}")
    logger.info(f"🪣 Bucket: {bucket_id}")
    logger.info(f"🧠 Model: ResNet-50 (512D vectors)")
    
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
            
            # Extract 512D features
            logger.info("   🧠 Extracting 512D features with ResNet-50...")
            features_list = feature_extractor.extract_features(image)
            logger.info(f"   Extracted {len(features_list)}D feature vector")
            
            # Read image as bytes
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            # Upload to Appwrite
            logger.info(f"    Uploading to Appwrite bucket: {bucket_id}...")
            result = retrieval.upload_image(
                image_data=image_bytes,
                filename=image_path.name,
                category=category,
                features=features_list
            )
            
            if result:
                success += 1
                logger.info(f"   SUCCESS - ID: {result.get('image_id', 'N/A')[:8]}...")
            else:
                failed += 1
                logger.error("   Upload failed")
            
            time.sleep(0.3)  # Rate limiting
            
        except Exception as e:
            failed += 1
            logger.error(f"   Error: {e}")
    
    # Summary
    elapsed = time.time() - start_time
    
    logger.info("\n" + "="*70)
    logger.info("HEALTHCARE UPLOAD SUMMARY")
    logger.info("="*70)
    logger.info(f"Successful: {success}")
    logger.info(f"Failed: {failed}")
    logger.info(f"📁 Total: {len(image_files)}")
    logger.info(f"⏱️  Time: {elapsed:.2f}s ({elapsed/max(len(image_files), 1):.2f}s per image)")
    logger.info("="*70)
    
    return success, failed


if __name__ == "__main__":
    try:
        config.validate()
        upload_healthcare_images()
        logger.info("\nDone! View at: https://fra.cloud.appwrite.io/console")
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
