"""
Surveillance Images Uploader for Appwrite
Uploads surveillance images to Appwrite storage and extracts features
"""

import os
import sys
from pathlib import Path
from PIL import Image
import logging

from config import config
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval
from unified_feature_extractor import UnifiedFeatureExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('surveillance_upload.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def upload_surveillance_images(image_dir: str = "data/professional_images/surveillance"):
    """
    Upload surveillance images to Appwrite
    
    Args:
        image_dir: Directory containing surveillance images
    """
    try:
        # Initialize components
        logger.info("🚀 Initializing Surveillance Uploader...")
        
        feature_extractor = UnifiedFeatureExtractor(
            model_path=config.MODEL_WEIGHTS_PATH,
            feature_dim=config.FEATURE_DIMENSION
        )
        logger.info("✅ Feature extractor initialized")
        
        retrieval_system = AppwriteQuantumRetrieval()
        logger.info("✅ Appwrite system initialized")
        
        # Get image files
        image_path = Path(image_dir)
        if not image_path.exists():
            logger.error(f"❌ Directory not found: {image_dir}")
            return
        
        image_files = list(image_path.glob("*.jpg")) + list(image_path.glob("*.png")) + list(image_path.glob("*.jpeg"))
        
        if not image_files:
            logger.warning(f"⚠️  No images found in {image_dir}")
            return
        
        logger.info(f"📁 Found {len(image_files)} surveillance images")
        
        # Upload images
        success_count = 0
        error_count = 0
        
        for idx, image_file in enumerate(image_files, 1):
            try:
                logger.info(f"\n[{idx}/{len(image_files)}] Processing: {image_file.name}")
                
                # Load image
                image = Image.open(image_file).convert('RGB')
                
                # Extract features
                logger.info("🧠 Extracting features...")
                features = feature_extractor.extract_features(image)
                features_list = features.cpu().numpy().tolist()
                
                # Read image data
                with open(image_file, 'rb') as f:
                    image_data = f.read()
                
                # Upload to Appwrite
                logger.info("📤 Uploading to Appwrite...")
                result = retrieval_system.upload_image(
                    image_data=image_data,
                    filename=image_file.name,
                    category='surveillance',
                    features=features_list
                )
                
                logger.info(f"✅ Upload successful: {result['image_id']}")
                success_count += 1
                
            except Exception as e:
                logger.error(f"❌ Error processing {image_file.name}: {e}")
                error_count += 1
                continue
        
        # Summary
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 Upload Summary")
        logger.info(f"{'='*60}")
        logger.info(f"✅ Successful: {success_count}")
        logger.info(f"❌ Errors: {error_count}")
        logger.info(f"📁 Total: {len(image_files)}")
        logger.info(f"{'='*60}\n")
        
    except Exception as e:
        logger.error(f"❌ Upload process failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    try:
        config.validate()
        
        # Check for custom directory
        if len(sys.argv) > 1:
            image_dir = sys.argv[1]
        else:
            image_dir = "data/professional_images/surveillance"
        
        upload_surveillance_images(image_dir)
        
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        sys.exit(1)
