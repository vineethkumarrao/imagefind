import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Quantum Image Retrieval System"""
    
    # Appwrite Configuration
    APPWRITE_ENDPOINT = os.getenv('APPWRITE_ENDPOINT', 'https://fra.cloud.appwrite.io/v1')
    APPWRITE_PROJECT_ID = os.getenv('APPWRITE_PROJECT_ID', '68eed0ee0033a7ceca80')
    APPWRITE_API_KEY = os.getenv('APPWRITE_API_KEY', '')
    
    # Appwrite Database
    APPWRITE_DATABASE_ID = os.getenv('APPWRITE_DATABASE_ID', 'quantum-images-db')
    APPWRITE_COLLECTION_ID = os.getenv('APPWRITE_COLLECTION_ID', 'feature-vectors')
    
    # Aliases for convenience
    DATABASE_ID = APPWRITE_DATABASE_ID
    COLLECTION_ID = APPWRITE_COLLECTION_ID
    
    # Appwrite Storage Buckets
    APPWRITE_BUCKET_HEALTHCARE = os.getenv('APPWRITE_BUCKET_HEALTHCARE', 'healthcare-images')
    APPWRITE_BUCKET_SATELLITE = os.getenv('APPWRITE_BUCKET_SATELLITE', 'satellite-images')
    APPWRITE_BUCKET_SURVEILLANCE = os.getenv('APPWRITE_BUCKET_SURVEILLANCE', 'surveillance-images')
    
    # Model Configuration
    MODEL_WEIGHTS_PATH = os.getenv('MODEL_WEIGHTS_PATH', 'consistent_resnet50_8d.pth')
    
    # Feature extraction
    FEATURE_EXTRACTOR = 'resnet50'  # Options: 'resnet50', 'vgg16'
    FEATURE_DIMENSION = 2048         # Dimension of feature vectors (ResNet-50 native)
    
    # Quantum Configuration
    USE_QUANTUM_INSPIRED = os.getenv('USE_QUANTUM_INSPIRED', 'True').lower() == 'true'
    N_ENCODING_QUBITS = int(os.getenv('N_ENCODING_QUBITS', '3'))
    N_AUXILIARY_QUBITS = int(os.getenv('N_AUXILIARY_QUBITS', '7'))
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '8000'))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Confidence Thresholds
    HIGH_CONFIDENCE_THRESHOLD = float(os.getenv('HIGH_CONFIDENCE_THRESHOLD', '0.95'))
    GOOD_CONFIDENCE_THRESHOLD = float(os.getenv('GOOD_CONFIDENCE_THRESHOLD', '0.0'))
    MINIMUM_MATCH_THRESHOLD = float(os.getenv('MINIMUM_MATCH_THRESHOLD', '0.85'))
    
    # Bucket mapping
    CATEGORY_BUCKET_MAP = {
        'healthcare': APPWRITE_BUCKET_HEALTHCARE,
        'satellite': APPWRITE_BUCKET_SATELLITE,
        'surveillance': APPWRITE_BUCKET_SURVEILLANCE
    }
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_vars = {
            'APPWRITE_ENDPOINT': cls.APPWRITE_ENDPOINT,
            'APPWRITE_PROJECT_ID': cls.APPWRITE_PROJECT_ID,
            'APPWRITE_API_KEY': cls.APPWRITE_API_KEY,
        }
        
        missing = [key for key, value in required_vars.items() if not value]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True

# Create config instance
config = Config()
