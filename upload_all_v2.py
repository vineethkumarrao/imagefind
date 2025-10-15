"""
Master Upload Script for All Image Categories
Uploads healthcare, satellite, and surveillance images with 512D ResNet-50 vectors
"""

import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_upload_script(script_name: str, category: str) -> bool:
    """Run an upload script"""
    try:
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting {category} image upload...")
        logger.info(f"{'='*60}\n")
        
        # Import and run the script
        if script_name == 'healthcare':
            from upload_healthcare import main
        elif script_name == 'satellite':
            from upload_satellite import main
        elif script_name == 'surveillance':
            from upload_surveillance import main
        else:
            raise ValueError(f"Unknown script: {script_name}")
        
        main()
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ {category} upload completed successfully!")
        logger.info(f"{'='*60}\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ {category} upload failed: {e}")
        return False

def main():
    """Main upload orchestrator"""
    logger.info("\n" + "="*60)
    logger.info("QUANTUM IMAGE RETRIEVAL SYSTEM - MASS UPLOAD")
    logger.info("="*60)
    logger.info("Uploading all images with 512D ResNet-50 vectors")
    logger.info("Categories: Healthcare, Satellite, Surveillance")
    logger.info("="*60 + "\n")
    
    results = {
        'healthcare': False,
        'satellite': False,
        'surveillance': False
    }
    
    # Upload each category
    results['healthcare'] = run_upload_script('healthcare', 'Healthcare (X-Ray)')
    results['satellite'] = run_upload_script('satellite', 'Satellite')
    results['surveillance'] = run_upload_script('surveillance', 'Surveillance')
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("UPLOAD SUMMARY")
    logger.info("="*60)
    
    for category, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        logger.info(f"{category.capitalize()}: {status}")
    
    total_success = sum(results.values())
    logger.info(f"\nTotal: {total_success}/3 categories uploaded successfully")
    logger.info("="*60 + "\n")
    
    if total_success == 3:
        logger.info("🎉 All images uploaded successfully!")
        logger.info("System ready for quantum-enhanced image retrieval")
    else:
        logger.warning("⚠️ Some uploads failed. Check logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
