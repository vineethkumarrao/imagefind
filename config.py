import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Quantum Image Retrieval System"""
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', '')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', '')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', '')
    
    # Pinecone Configuration
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', '')
    PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')
    PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME', 'quantum-images-prod')
    
    # Model Configuration
    MODEL_WEIGHTS_PATH = os.getenv('MODEL_WEIGHTS_PATH', 'consistent_resnet50_8d.pth')
    
    # Feature extraction
    FEATURE_EXTRACTOR = 'resnet50'  # Options: 'resnet50', 'vgg16'
    FEATURE_DIMENSION = int(os.getenv('FEATURE_DIMENSION', '2048'))  # 2048 or 512
    
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
    GOOD_CONFIDENCE_THRESHOLD = float(os.getenv('GOOD_CONFIDENCE_THRESHOLD', '0.85'))
    MINIMUM_MATCH_THRESHOLD = float(os.getenv('MINIMUM_MATCH_THRESHOLD', '0.80'))
    
    # Image categories
    CATEGORIES = ['healthcare', 'satellite', 'surveillance']
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_vars = {
            'CLOUDINARY_CLOUD_NAME': cls.CLOUDINARY_CLOUD_NAME,
            'CLOUDINARY_API_KEY': cls.CLOUDINARY_API_KEY,
            'CLOUDINARY_API_SECRET': cls.CLOUDINARY_API_SECRET,
            'PINECONE_API_KEY': cls.PINECONE_API_KEY,
        }
        
        missing = [key for key, value in required_vars.items() if not value]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True

# Create config instance
config = Config()
config.validate()
