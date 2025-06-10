# PostgreSQL Configuration for Daily Post Flask App
# Replace your existing database configuration with this

import os

# PostgreSQL Database Configuration
POSTGRESQL_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'daily_post',
    'user': 'dailypost_user',
    'password': 'dailypost123'
}

# SQLAlchemy Database URI for PostgreSQL
POSTGRESQL_URI = f"postgresql://{POSTGRESQL_CONFIG['user']}:{POSTGRESQL_CONFIG['password']}@{POSTGRESQL_CONFIG['host']}:{POSTGRESQL_CONFIG['port']}/{POSTGRESQL_CONFIG['database']}"

# Update your app.py with this configuration:
# Replace this line:
#   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
# With this line:
#   app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_URI

# Or use environment variable for production:
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', POSTGRESQL_URI)
