# PostgreSQL Configuration for Flask
# Add this to your app.py

import os

# PostgreSQL Database Configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'daily_post',  # Change this to your database name
    'user': 'postgres',
    'password': os.environ.get('POSTGRES_PASSWORD', 'your_password_here')
}

# SQLAlchemy Database URI for PostgreSQL
POSTGRESQL_URI = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

# Update your Flask app configuration:
# app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_URI

# Example usage in app.py:
# Replace this line:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
# With this line:
# app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_URI
