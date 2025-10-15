"""Verify we're working with the correct image"""
from PIL import Image
import hashlib

# Calculate hash of the test image
img_path = 'testingimages/xray/NORMAL2-IM-0350-0001.jpeg'
with open(img_path, 'rb') as f:
    img_bytes = f.read()
    img_hash = hashlib.md5(img_bytes).hexdigest()

print(f"Image path: {img_path}")
print(f"MD5 hash: {img_hash}")
print(f"File size: {len(img_bytes)} bytes")

# Load and check image properties
img = Image.open(img_path)
print(f"Image size: {img.size}")
print(f"Image mode: {img.mode}")
print(f"Image format: {img.format}")
