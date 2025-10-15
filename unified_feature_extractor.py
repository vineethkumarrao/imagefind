"""
Unified Feature Extractor using ResNet-50
Extracts 512D feature vectors from images for high-quality similarity matching
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
import logging

logger = logging.getLogger(__name__)


class UnifiedFeatureExtractor:
    """Extract features from images using pre-trained ResNet-50"""
    
    def __init__(self, feature_dim=512):
        """
        Initialize the feature extractor
        
        Args:
            feature_dim: Dimension of output features (default: 512)
        """
        logger.info(f"🔧 Initializing ResNet-50 feature extractor ({feature_dim}D)...")
        
        self.feature_dim = feature_dim
        
        # Load pre-trained ResNet-50
        logger.info("📦 Loading pre-trained ResNet-50 model...")
        resnet = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
        
        # Remove the final classification layer (FC) to get features
        # ResNet-50 outputs 2048D features before the final FC layer
        self.model = nn.Sequential(*list(resnet.children())[:-1])
        
        # Add adaptive pooling and dimension reduction if needed
        if feature_dim != 2048:
            self.model = nn.Sequential(
                self.model,
                nn.Flatten(),
                nn.Linear(2048, feature_dim),
                nn.ReLU(),
                nn.BatchNorm1d(feature_dim)
            )
        else:
            self.model = nn.Sequential(
                self.model,
                nn.Flatten()
            )
        
        # Set to evaluation mode
        self.model.eval()
        
        # Define image preprocessing (ImageNet normalization)
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],  # ImageNet mean
                std=[0.229, 0.224, 0.225]     # ImageNet std
            )
        ])
        
        # Move to GPU if available
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.model.to(self.device)
        
        logger.info(f"✅ Feature extractor ready (Device: {self.device})")
        logger.info(f"   Input: 224x224 RGB images")
        logger.info(f"   Output: {feature_dim}D feature vectors")
        logger.info(f"   Model: ResNet-50 (ImageNet pre-trained)")
    
    def extract_features(self, image):
        """
        Extract features from an image
        
        Args:
            image: PIL Image or path to image
            
        Returns:
            list: Feature vector (512D by default)
        """
        # Load image if path is provided
        if isinstance(image, str):
            image = Image.open(image).convert('RGB')
        elif not isinstance(image, Image.Image):
            raise ValueError("Image must be PIL Image or path string")
        
        # Ensure RGB mode
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Preprocess image
        image_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
        
        # Extract features
        with torch.no_grad():
            features = self.model(image_tensor)
        
        # Convert to numpy and then to list
        features = features.cpu().squeeze().numpy()
        
        # Normalize features (L2 normalization for better similarity comparison)
        features = features / (np.linalg.norm(features) + 1e-8)
        
        # Convert to Python list
        feature_list = features.tolist()
        
        return feature_list
    
    def extract_batch_features(self, images):
        """
        Extract features from multiple images (batch processing)
        
        Args:
            images: List of PIL Images or paths
            
        Returns:
            list: List of feature vectors
        """
        batch_tensors = []
        
        for image in images:
            # Load image if path
            if isinstance(image, str):
                image = Image.open(image).convert('RGB')
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Preprocess
            tensor = self.preprocess(image)
            batch_tensors.append(tensor)
        
        # Stack into batch
        batch = torch.stack(batch_tensors).to(self.device)
        
        # Extract features
        with torch.no_grad():
            features = self.model(batch)
        
        # Normalize and convert to list
        features = features.cpu().numpy()
        features = features / (np.linalg.norm(features, axis=1, keepdims=True) + 1e-8)
        
        return features.tolist()
    
    def get_feature_dim(self):
        """Get the dimension of feature vectors"""
        return self.feature_dim
