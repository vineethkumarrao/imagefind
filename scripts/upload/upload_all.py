"""
Master Upload Script - Upload All Testing Images
Uploads healthcare, satellite, and surveillance images with 512D embeddings
"""

import time
import logging

from config import config
from upload_healthcare import upload_healthcare_images
from upload_satellite import upload_satellite_images
from upload_surveillance import upload_surveillance_images

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def upload_all_categories():
    """Upload all image categories"""
    
    logger.info("\n" + "#"*70)
    logger.info("🚀 MASTER UPLOAD - ALL CATEGORIES")
    logger.info("#"*70)
    logger.info("Model: ResNet-50 (512D feature vectors)")
    logger.info(" Target: Appwrite Cloud (Frankfurt)")
    logger.info("🗂️  Categories: Healthcare, Satellite, Surveillance")
    logger.info("#"*70 + "\n")
    
    start_time = time.time()
    results = {}
    
    # Upload Healthcare
    try:
        logger.info("\n🏥 Starting Healthcare upload...")
        success, failed = upload_healthcare_images()
        results['healthcare'] = {'success': success, 'failed': failed}
    except Exception as e:
        logger.error(f"Healthcare upload error: {e}")
        results['healthcare'] = {'success': 0, 'failed': 0}
    
    # Upload Satellite
    try:
        logger.info("\n🛰️  Starting Satellite upload...")
        success, failed = upload_satellite_images()
        results['satellite'] = {'success': success, 'failed': failed}
    except Exception as e:
        logger.error(f"Satellite upload error: {e}")
        results['satellite'] = {'success': 0, 'failed': 0}
    
    # Upload Surveillance
    try:
        logger.info("\n📹 Starting Surveillance upload...")
        success, failed = upload_surveillance_images()
        results['surveillance'] = {'success': success, 'failed': failed}
    except Exception as e:
        logger.error(f"Surveillance upload error: {e}")
        results['surveillance'] = {'success': 0, 'failed': 0}
    
    # Final Summary
    elapsed = time.time() - start_time
    total_success = sum(r['success'] for r in results.values())
    total_failed = sum(r['failed'] for r in results.values())
    
    logger.info("\n" + "#"*70)
    logger.info("🎉 MASTER UPLOAD COMPLETE!")
    logger.info("#"*70)
    
    for category, stats in results.items():
        logger.info(f"{category.upper():15} - {stats['success']:3} "
                   f"| {stats['failed']:3}")
    
    logger.info("-"*70)
    logger.info(f"{'TOTAL':15} - {total_success:3} | {total_failed:3}")
    logger.info(f"{'TIME':15} - ⏱️  {elapsed:.2f}s")
    logger.info("#"*70)
    
    logger.info("\nAll images uploaded with 512D feature vectors!")
    logger.info("🌐 View at: https://fra.cloud.appwrite.io/console")
    logger.info("Test similarity search in your app!")


if __name__ == "__main__":
    try:
        config.validate()
        upload_all_categories()
    except KeyboardInterrupt:
        logger.warning("\nUpload interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
