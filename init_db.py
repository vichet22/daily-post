#!/usr/bin/env python3
"""
Database initialization script for Daily Post
"""

from app import app, db, Post
from datetime import datetime

def init_database():
    """Initialize the database with tables and sample data"""
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        print("Database tables created successfully!")
        
        # Add sample data
        sample_posts = [
            Post(title="Welcome to Daily Post", 
                 content="This is your first post on Daily Post! This platform allows you to share news, stories, and updates with your audience. You can create, edit, and manage posts through the admin interface.",
                 author="Admin", category="Announcement", featured=True, 
                 image_url="https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&h=400&fit=crop"),
            Post(title="Getting Started Guide", 
                 content="Here's how to use Daily Post: 1. Visit /admin to access the admin panel 2. Create new posts with the 'New Post' button 3. Edit or delete existing posts 4. Mark important posts as featured to highlight them on the homepage.",
                 author="Admin", category="Guide", featured=True,
                 image_url="https://images.unsplash.com/photo-1432888622747-4eb9a8efeb07?w=800&h=400&fit=crop"),
            Post(title="Features Overview", 
                 content="Daily Post comes with many features: responsive design, search functionality, category filtering, featured posts, admin interface, and a clean modern UI. Perfect for news sites, blogs, or any content-driven website.",
                 author="Admin", category="Features", featured=False,
                 image_url="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop")
        ]
        
        for post in sample_posts:
            db.session.add(post)
        
        db.session.commit()
        print(f"Added {len(sample_posts)} sample posts!")
        print("Database initialization complete!")

if __name__ == '__main__':
    init_database()
