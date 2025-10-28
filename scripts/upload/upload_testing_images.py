"""
Upload Testing Images to Appwrite with 512D Feature Extraction
Handles xray (healthcare), satellite, and survey (surveillance) images
"""

import os
import time
from pathlib import Path
from PIL import Image
import logging

from config import config
from unified_feature_extractor import UnifiedFeatureExtractor
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestingImagesUploader:
    """Upload testing images with 512D feature extraction"""
    
    def __init__(self):
        """Initialize uploader"""
        logger.info("🚀 Initializing Testing Images Uploader...")
        
        # Initialize feature extractor (512D)
        logger.info("📦 Loading ResNet-50 feature extractor (512D)...")
        self.feature_extractor = UnifiedFeatureExtractor(feature_dim=512)
        
        # Initialize Appwrite
        logger.info("☁️  Connecting to Appwrite...")
        self.retrieval = AppwriteQuantumRetrieval()
        
        # Category mappings
        self.category_map = {
            'xray': 'healthcare',
            'satellite': 'satellite',
            'survey': 'surveillance'
        }
        
        self.bucket_map = {
            'healthcare': 'healthcare-images',
            'satellite': 'satellite-images',
            'surveillance': 'surveillance-images'
        }
        
        logger.info("✅ Uploader initialized")
        logger.info(f"   Feature dimension: {self.feature_extractor.get_feature_dim()}D")
        logger.info(f"   Appwrite: {config.APPWRITE_ENDPOINT}")
    
    def upload_category(self, category_folder: str, category_name: str):
        """
        Upload all images from a category folder
        
        Args:
            category_folder: Path to folder containing images
            category_name: Category name (xray, satellite, survey)
        """
        folder_path = Path(category_folder)
        
        if not folder_path.exists():
            logger.error(f"❌ Folder not found: {folder_path}")
            return 0, 0
        
        # Get mapped category for database
        db_category = self.category_map.get(category_name, category_name)
        bucket_id = self.bucket_map.get(db_category, f"{db_category}-images")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"📁 Processing {category_name.upper()} images")
        logger.info(f"   Folder: {folder_path}")
        logger.info(f"   Category: {db_category}")
        logger.info(f"   Bucket: {bucket_id}")
        logger.info(f"{'='*60}\n")
        
        # Get all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        image_files = [
            f for f in folder_path.iterdir()
            if f.suffix.lower() in image_extensions
        ]
        
        if not image_files:
            logger.warning(f"⚠️  No images found in {folder_path}")
            return 0, 0
        
        logger.info(f"📊 Found {len(image_files)} images to upload")
        
        success_count = 0
        error_count = 0
        
        for idx, image_file in enumerate(image_files, 1):
            try:
                logger.info(f"\n[{idx}/{len(image_files)}] {image_file.name}")
                
                # Load image
                image = Image.open(image_file).convert('RGB')
                logger.info(f"   📏 Size: {image.size}")
                
                # Extract 512D features
                logger.info("   🔍 Extracting 512D features...")
                features = self.feature_extractor.extract_features(image)
                logger.info(f"   ✅ Features: {len(features)}D vector (normalized)")
                
                # Upload to Appwrite
                logger.info("   ☁️  Uploading to Appwrite...")
                result = self.retrieval.upload_image(
                    image_path=str(image_file),
                    category=db_category,
                    features_list=features,
                    bucket_id=bucket_id
                )
                
                if result:
                    success_count += 1
                    image_id = result.get('image_id', 'N/A')
                    logger.info(f"   ✅ SUCCESS - ID: {image_id}")
                else:
                    error_count += 1
                    logger.error("   ❌ FAILED - No result")
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                error_count += 1
                logger.error(f"   ❌ ERROR: {e}")
                continue
        
        # Summary
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 {category_name.upper()} SUMMARY:")
        logger.info(f"   ✅ Successful: {success_count}")
        logger.info(f"   ❌ Failed: {error_count}")
        logger.info(f"   📁 Total: {len(image_files)}")
        logger.info(f"{'='*60}\n")
        
        return success_count, error_count
    
    def upload_all(self, base_folder: str = "testingimages"):
        """
        Upload all testing images from all categories
        
        Args:
            base_folder: Base folder containing category subfolders
        """
        base_path = Path(base_folder)
        
        if not base_path.exists():
            logger.error(f"❌ Base folder not found: {base_path}")
            return
        
        logger.info(f"\n{'#'*60}")
        logger.info("🚀 STARTING BULK UPLOAD WITH 512D EMBEDDINGS")
        logger.info(f"   Base folder: {base_path.absolute()}")
        logger.info(f"   Appwrite: {config.APPWRITE_ENDPOINT}")
        logger.info(f"   Model: ResNet-50 (512D features)")
        logger.info(f"{'#'*60}\n")
        
        start_time = time.time()
        
        # Upload each category
        total_success = 0
        total_failed = 0
        
        categories = [
            ('xray', 'xray'),
            ('satellite', 'satellite'),
            ('survey', 'survey')
        ]
        
        for folder_name, category_name in categories:
            folder_path = base_path / folder_name
            
            if folder_path.exists():
                success, failed = self.upload_category(
                    str(folder_path),
                    category_name
                )
                total_success += success
                total_failed += failed
            else:
                logger.warning(f"⚠️  Skipping: {folder_path}")
        
        elapsed = time.time() - start_time
        
        # Final summary
        logger.info(f"\n{'#'*60}")
        logger.info("🎉 UPLOAD COMPLETE!")
        logger.info(f"   ✅ Total successful: {total_success}")
        logger.info(f"   ❌ Total failed: {total_failed}")
        logger.info(f"   ⏱️  Time: {elapsed:.2f}s")
        avg_time = elapsed / max(total_success + total_failed, 1)
        logger.info(f"   📊 Average: {avg_time:.2f}s per image")
        logger.info(f"{'#'*60}\n")
        
        # Get final statistics
        logger.info("📊 Fetching database statistics...")
        try:
            stats = self.retrieval.get_statistics()
            logger.info(f"\n{'='*60}")
            logger.info("DATABASE STATISTICS:")
            logger.info(f"   Total images: {stats.get('total_images', 0)}")
            logger.info(f"   Healthcare: {stats.get('healthcare', 0)}")
            logger.info(f"   Satellite: {stats.get('satellite', 0)}")
            logger.info(f"   Surveillance: {stats.get('surveillance', 0)}")
            logger.info(f"{'='*60}\n")
        except Exception as e:
            logger.error(f"❌ Error fetching stats: {e}")


def main():
    """Main function"""
    try:
        # Validate config
        config.validate()
        
        # Create uploader
        uploader = TestingImagesUploader()
        
        # Upload all images
        uploader.upload_all("testingimages")
        
        logger.info("✅ All done!")
        logger.info("   Images stored in Appwrite with 512D vectors")
        logger.info("   Same model will be used for searching")
        logger.info("🌐 View at: https://fra.cloud.appwrite.io/console")
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Upload interrupted by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
