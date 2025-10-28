"""
Healthcare Images Uploader
Uploads healthcare images to Cloudinary and stores vectors in Pinecone
"""

import sys
from pathlib import Path
from PIL import Image
import logging

from config import config
from services.cloudinary_service import CloudinaryImageService
from services.pinecone_service import PineconeVectorService
from ml.unified_feature_extractor import UnifiedFeatureExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('healthcare_upload.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def upload_healthcare_images(image_dir: str = "data/testingimages/healthcare"):
    """
    Upload healthcare images to Cloudinary and Pinecone
    
    Args:
        image_dir: Directory containing healthcare images
    """
    try:
        # Initialize components
        logger.info("Initializing Healthcare Uploader...")
        feature_extractor = UnifiedFeatureExtractor(
            feature_dim=config.FEATURE_DIMENSION,
            use_amp=True
        )
        logger.info("Feature extractor initialized")
        
        cloudinary_service = CloudinaryImageService()
        pinecone_service = PineconeVectorService()
        logger.info("Cloud services initialized")
        
        # Get image files
        image_path = Path(image_dir)
        if not image_path.exists():
            logger.error(f"Directory not found: {image_dir}")
            return
        
        image_files = (list(image_path.glob("*.jpg")) + 
                      list(image_path.glob("*.png")) + 
                      list(image_path.glob("*.jpeg")))
        
        if not image_files:
            logger.warning(f"No images found in {image_dir}")
            return
        
        logger.info(f"Found {len(image_files)} healthcare images")
        
        # Upload images
        success_count = 0
        error_count = 0
        
        for idx, image_file in enumerate(image_files, 1):
            try:
                logger.info(f"\n[{idx}/{len(image_files)}] Processing: {image_file.name}")
                
                # Load image
                image = Image.open(image_file).convert('RGB')
                
                # Extract features
                logger.info("Extracting features...")
                features = feature_extractor.extract_features(image)
                
                # Read image data
                with open(image_file, 'rb') as f:
                    image_data = f.read()
                
                # Upload to Cloudinary
                logger.info("Uploading to Cloudinary...")
                result = cloudinary_service.upload_image(
                    image_data,
                    image_file.name,
                    'healthcare'
                )
                
                # Store in Pinecone
                logger.info("Storing in Pinecone...")
                vector_id = result['public_id'].replace('/', '_')
                metadata = {
                    'filename': image_file.name,
                    'category': 'healthcare',
                    'cloudinary_url': result['secure_url']
                }
                pinecone_service.upsert_vector(vector_id, features, metadata)
                
                logger.info(f"Upload successful: {result['public_id']}")
                success_count += 1
                
            except Exception as e:
                logger.error(f"Error processing {image_file.name}: {e}")
                error_count += 1
                continue
        
        # Summary
        logger.info(f"\n{'='*60}")
        logger.info("Upload Summary")
        logger.info(f"{'='*60}")
        logger.info(f"Successful: {success_count}")
        logger.info(f"Errors: {error_count}")
        logger.info(f"Total: {len(image_files)}")
        logger.info(f"{'='*60}\n")
        
    except Exception as e:
        logger.error(f"Upload process failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    try:
        config.validate()
        
        # Check for custom directory
        if len(sys.argv) > 1:
            image_dir = sys.argv[1]
        else:
            image_dir = "data/professional_images/healthcare"
        
        upload_healthcare_images(image_dir)
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
