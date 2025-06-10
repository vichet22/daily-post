#!/usr/bin/env python3
"""
Daily Post - Production Entry Point
This file serves as the main entry point for production deployment
"""

import os
import sys

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import the Flask app from backend
from backend.app import app, db

# Production configuration
if __name__ == '__main__':
    # Initialize database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created/verified!")
        except Exception as e:
            print(f"⚠️ Database initialization warning: {e}")
    
    # Get port from environment (for Railway, Heroku, etc.)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=False)
