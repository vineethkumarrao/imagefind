#!/usr/bin/env python3
"""
Main entry point for running the Quantum Image Retrieval backend server.

Usage:
    python main.py              # Start server
    python -m uvicorn main:app --reload  # With reload
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from backend.backend_server import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
